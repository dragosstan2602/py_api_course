from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint
from datetime import datetime
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOutput(BaseModel):
    id: int
    email: EmailStr
    # created_at: datetime
    
    class Config:
        orm_mode = True
        
class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    owner_id: int
    owner: UserOutput
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
      
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    direction: int = Field(..., ge=0, le=1)