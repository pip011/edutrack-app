from datetime                           import datetime
from typing                             import TYPE_CHECKING, List

from sqlalchemy                         import ForeignKey, Table, Column
from sqlalchemy.orm                     import Mapped
from sqlalchemy.orm                     import mapped_column
from sqlalchemy.orm                     import relationship

from ..db                               import Base
from .secondary_models                  import subject_teacher_association

if TYPE_CHECKING:
    from .subject_model                 import Subject
    from .user_model                    import User


class Teacher(Base):
    __tablename__ = "teachers"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    birth_date: Mapped[datetime] = mapped_column(nullable=True)
    
    subjects: Mapped[List[Subject] | None] = relationship(
        secondary=subject_teacher_association, 
        back_populates="teachers"
    )
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship(back_populates="teacher")