from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import create_access_token, get_current_user
from app.schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse, ProfileResponse
from app.schemas.blog import BlogCreate, BlogResponse
from app.services.auth import create_user, authenticate_user, get_user_by_email
from app.services.blog import create_blog, get_all_blogs
from app.tasks.celery_app import send_email_task

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, request.email, request.password)
    access_token = create_access_token(data={"mail": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=ProfileResponse)
def read_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user_by_email(current_user["email"], db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return {
        "message": "Profile fetched successfully",
        "email": user.email,
        "username": user.username,
        "auth_provider": user.auth_provider,
        "profile_picture": user.profile_picture
    }

@router.post("/posts", response_model=BlogResponse)
def create_blog_post(post: BlogCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_post = create_blog(post, db)
    send_email_task.delay(new_post.title, new_post.description, current_user["email"])
    return new_post

@router.get("/posts", response_model=List[BlogResponse])
def read_all_posts(db: Session = Depends(get_db)):
    return get_all_blogs(db)
