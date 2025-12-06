from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TeacherId(BaseModel):
    id: int

class Teacher(BaseModel):
    id: int
    full_name: str | None
    birth_date: datetime | None
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)
    
class TeacherUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None