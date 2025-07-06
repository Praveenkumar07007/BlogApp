import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.settings import settings

def send_blog_email(blog_title: str, blog_description: str, receiver_email: str):
    if not settings.SMTP_EMAIL or not settings.SMTP_PASSWORD:
        return "SMTP not configured"

    subject = f"New Blog Created: {blog_title}"
    body = f"""
    Hi,

    A new blog has been created:

    Title: {blog_title}
    Description: {blog_description}

    Regards,
    Your FastAPI App
    """

    msg = MIMEMultipart()
    msg["From"] = settings.SMTP_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.SMTP_EMAIL, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_EMAIL, receiver_email, msg.as_string())
        return f"Email sent successfully to {receiver_email}"
    except Exception as e:
        return f"Error sending email: {e}"
