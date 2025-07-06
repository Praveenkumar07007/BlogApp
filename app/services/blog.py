from sqlalchemy.orm import Session
from app.models.user import Blog
from app.schemas.blog import BlogCreate

def create_blog(blog_data: BlogCreate, db: Session):
    blog = Blog(
        title=blog_data.title,
        description=blog_data.description
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def get_all_blogs(db: Session):
    return db.query(Blog).all()
