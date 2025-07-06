from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

def create_user(user_data: UserCreate, db: Session):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_pwd = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pwd,
        auth_provider="local"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not verify_password(password, str(user.password)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    return user

def get_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

def create_or_update_google_user(google_id: str, name: str, email: str, picture: Optional[str], db: Session):
    user = db.query(User).filter(User.google_id == google_id).first()

    if user:
        user.username = name
        user.profile_picture = picture
        db.commit()
        db.refresh(user)
        return user

    user = db.query(User).filter(User.email == email).first()
    if user:
        user.google_id = google_id
        user.profile_picture = picture
        user.auth_provider = "google"
        db.commit()
        db.refresh(user)
        return user

    user = User(
        username=name,
        email=email,
        google_id=google_id,
        profile_picture=picture,
        auth_provider="google",
        password=None
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
