from celery import Celery
from app.config.settings import settings
from app.services.email import send_blog_email

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

@celery_app.task
def send_email_task(blog_title: str, blog_description: str, receiver_email: str):
    return send_blog_email(blog_title, blog_description, receiver_email)
