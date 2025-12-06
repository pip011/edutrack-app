from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from backend.enums import UserRole
from backend.schemas.teacher_schema import TeacherUpdate
from backend.schemas.student_schema import StudentUpdate


class UserCreate(BaseModel):
    username: str = Field(..., example="student2000")
    password: str = Field(..., min_length=6, example="mypassword123")
    role: Optional[UserRole] = Field(default=UserRole.student, example="teacher")
    
class UserResponse(BaseModel):
    ok: bool = True
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class UserId:
    user_id: int
    
class UserUpdate(BaseModel):
    student: Optional[StudentUpdate] = None
    teacher: Optional[TeacherUpdate] = None