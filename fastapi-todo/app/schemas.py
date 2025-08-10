from pydantic import BaseModel, Field
from typing import Optional
import enum 

class TaskStatus(str, enum.Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    first_name: str
    last_name: Optional[str] = None

class UserOut(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: Optional[str] = None

    class Config:
        from_attributes = True  

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.new  

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskOut(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  

class Token(BaseModel):
    access_token: str
    token_type: str

