from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateGrade(BaseModel):
    grade: int
    date: datetime
    student_id: int
    subject_id: int

class Grade(CreateGrade):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class GradesList(BaseModel):
    grades: list[Grade] = []
    
class GradesForSubject(BaseModel):
    subject_id: int
    month: int
    year: int
    
class GradeUpdate(BaseModel):
    grade: int