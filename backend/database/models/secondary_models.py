from sqlalchemy     import Table, Column, ForeignKey

from ..db    import Base


subject_teacher_association = Table(
    "subject_teacher_association",
    Base.metadata,
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
    Column("teacher_id", ForeignKey("teachers.id"), primary_key=True)
)