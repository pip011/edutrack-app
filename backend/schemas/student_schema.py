from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Student(BaseModel):
    id: int
    full_name: str | None
    birth_date: datetime | None
    user_id: int
    group_id: int | None 
    
    model_config = ConfigDict(from_attributes=True)
    
class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    birth_date: Optional[datetime] = None
    group_id: Optional[int] = None