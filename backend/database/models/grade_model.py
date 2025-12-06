from datetime                       import datetime
from typing                         import TYPE_CHECKING

from sqlalchemy                     import ForeignKey, String
from sqlalchemy.orm                 import Mapped
from sqlalchemy.orm                 import mapped_column
from sqlalchemy.orm                 import relationship

from ..db                           import Base

if TYPE_CHECKING:
    from .student_model             import Student


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(nullable=False)
    date: Mapped[datetime]  
    
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    student: Mapped[Student] = relationship(back_populates="grades")
    
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)