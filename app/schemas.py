from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ResourceCreate(BaseModel):
    name: str
    category: str
    location: str

class ResourceOut(ResourceCreate):
    id: int
    owner_id: int
    class Config:
        orm_mode = True

class BookingCreate(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime

class BookingOut(BookingCreate):
    id: int
    user_id: int
    class Config:
        orm_mode = True