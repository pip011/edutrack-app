from datetime                                   import datetime
from typing                                     import TYPE_CHECKING, List

from sqlalchemy                                 import ForeignKey
from sqlalchemy.orm                             import Mapped
from sqlalchemy.orm                             import mapped_column
from sqlalchemy.orm                             import relationship

from ..db                                       import Base

if TYPE_CHECKING:
    from .student_model                         import Student


class Group(Base):
    __tablename__ = "groups"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    year_start: Mapped[int]
    
    students: Mapped[List[Student] | None] = relationship(back_populates="group")