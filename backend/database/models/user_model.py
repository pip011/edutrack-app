from typing import TYPE_CHECKING
from sqlalchemy.orm                 import Mapped
from sqlalchemy.orm                 import mapped_column
from sqlalchemy.orm                 import relationship

from ..db                           import Base

if TYPE_CHECKING:
    from .student_model             import Student
    from .teacher_model             import Teacher

    
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="student", nullable=False)
    
    student: Mapped[Student | None] = relationship(back_populates="user")
    teacher: Mapped[Teacher | None] = relationship(back_populates="user")