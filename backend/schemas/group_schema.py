from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..schemas.student_schema import Student


class CreateGroup(BaseModel):
    name: str
    year_start: int
    
class Group(CreateGroup):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class GroupWithStudents(CreateGroup):
    id: int
    students: list[Student] = []
    
    model_config = ConfigDict(from_attributes=True)
    
class GroupsResponse(BaseModel):
    groups: list[GroupWithStudents]
    
class BindStudentToGroup(BaseModel):
    student_id: int
    group_id: int
    
class StudentId(BaseModel):
    student_id: int