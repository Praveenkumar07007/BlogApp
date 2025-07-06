from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.oauth import oauth
from app.core.security import create_access_token
from app.services.auth import create_or_update_google_user
from app.config.settings import settings
import httpx

router = APIRouter()

@router.get('/google/login')
async def google_login(request: Request):
    if oauth is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET."
        )

    redirect_uri = "http://localhost:8000/api/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/google/callback')
async def google_callback(request: Request, db: Session = Depends(get_db)):
    if oauth is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google OAuth not configured"
        )

    try:
        # Get authorization code from query parameters
        code = request.query_params.get('code')
        if not code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code not found"
            )

        # Exchange code for token manually using settings
        token_data = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:8000/api/google/callback'
        }

        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                'https://oauth2.googleapis.com/token',
                data=token_data
            )
            token_response.raise_for_status()
            token = token_response.json()

        # Get user info using access token
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization': f"Bearer {token['access_token']}"}
            )
            userinfo_response.raise_for_status()
            user_data = userinfo_response.json()

        # Extract user information
        google_id = user_data.get("id")
        name = user_data.get("name")
        email = user_data.get("email")
        picture = user_data.get("picture")

        if not google_id or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Required user information not available from Google"
            )

        if not name:
            name = email.split("@")[0]

        # Create or update user in database
        user = create_or_update_google_user(google_id, name, email, picture, db)

        # Create JWT token
        jwt_token = create_access_token(data={
            "mail": user.email,
            "user_id": user.id
        })

        return JSONResponse({
            "message": "Authentication successful via Google!",
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "auth_provider": user.auth_provider,
                "profile_picture": user.profile_picture
            }
        })

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth error: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication failed: {str(e)}"
        )
