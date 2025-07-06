from authlib.integrations.starlette_client import OAuth
from app.config.settings import settings
from typing import Optional

def create_oauth_client() -> Optional[OAuth]:
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        return None

    oauth = OAuth()
    oauth.register(
        name='google',
        client_id=settings.GOOGLE_CLIENT_ID,
        client_secret=settings.GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={
            'scope': 'openid email profile',
            'response_type': 'code'
        }
    )
    return oauth

oauth = create_oauth_client()
