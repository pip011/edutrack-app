from typing import List

from pydantic import BaseModel, ConfigDict

from ..schemas.teacher_schema import Teacher


class CreateSubject(BaseModel):
    name: str

class Subject(CreateSubject):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class SubjectWithTeachers(CreateSubject):
    id: int
    teachers: list[Teacher] = []
    
    model_config = ConfigDict(from_attributes=True)
    
class AllSubjectsResponse(BaseModel):
    subjects: list[SubjectWithTeachers] = []    
    
class BindSubjectTeacher(BaseModel):
    teacher_id: int
    subject_id: int