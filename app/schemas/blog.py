from pydantic import BaseModel
from datetime import datetime

class BlogCreate(BaseModel):
    title: str
    description: str

class BlogResponse(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
