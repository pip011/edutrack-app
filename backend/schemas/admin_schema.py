from pydantic import BaseModel, ConfigDict

from backend.schemas.teacher_schema import Teacher
from backend.schemas.student_schema import Student


class AdminUser(BaseModel):
    id: int 
    username: str
    role: str
    student: Student | None
    teacher: Teacher | None
        
    model_config = ConfigDict(from_attributes=True)
        
class UsersResponse(BaseModel):
    users: list[AdminUser]