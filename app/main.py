from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.database import Base, engine
from app.routers import auth, google_auth
from app.config.settings import settings

app = FastAPI(title="Blog API", version="1.0.0")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(google_auth.router, prefix="/api", tags=["google-auth"])

@app.get("/")
def root():
    return {"message": "Blog API is running!"}
