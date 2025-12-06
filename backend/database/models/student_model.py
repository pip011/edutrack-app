from datetime                       import datetime
from typing                         import TYPE_CHECKING, List

from sqlalchemy                     import ForeignKey
from sqlalchemy.orm                 import Mapped
from sqlalchemy.orm                 import mapped_column
from sqlalchemy.orm                 import relationship

from ..db                           import Base

if TYPE_CHECKING:
    from .grade_model               import Grade
    from .group_model               import Group
    from .user_model                import User


class Student(Base):
    __tablename__ = "students"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[datetime] = mapped_column(nullable=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User | None] = relationship(back_populates="student")
    
    group_id: Mapped[int | None] = mapped_column(ForeignKey("groups.id"), nullable=True)
    group: Mapped[Group | None] = relationship(back_populates="students")
    
    grades: Mapped[List[Grade]] = relationship(back_populates="student")