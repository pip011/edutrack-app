from typing                             import TYPE_CHECKING, List

from sqlalchemy                         import ForeignKey, Table, Column
from sqlalchemy.orm                     import Mapped
from sqlalchemy.orm                     import mapped_column
from sqlalchemy.orm                     import relationship

from ..db                               import Base
from .secondary_models                  import subject_teacher_association

if TYPE_CHECKING:
    from .teacher_model                 import Teacher


class Subject(Base):
    __tablename__ = "subjects"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    
    teachers: Mapped[List[Teacher] | None] = relationship(
        secondary=subject_teacher_association, 
        back_populates="subjects"
    )