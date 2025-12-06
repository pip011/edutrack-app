from sqlalchemy                         import ForeignKey, Table, Column
from sqlalchemy.orm                     import Mapped
from sqlalchemy.orm                     import mapped_column
from sqlalchemy.orm                     import relationship

from ..db                               import Base


class TeacherSubjectGroup(Base):
    __tablename__ = "teacher_subject_group"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)