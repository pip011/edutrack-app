from sqlalchemy import insert, select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models.secondary_models import subject_teacher_association

class TeacherSubjectRepository:
    @staticmethod
    async def bind_teacher_to_subject(data: dict, session: AsyncSession) -> bool:
        query = (
            select(subject_teacher_association)
            .where(
                subject_teacher_association.c.subject_id == data['subject_id'],
                subject_teacher_association.c.teacher_id == data['teacher_id'],
            )
        )

        result = await session.execute(query)
        exists = result.first()

        if exists:
            return False

        stmt = insert(subject_teacher_association).values(**data)

        await session.execute(stmt)
        await session.flush()

        return True
    
    @staticmethod
    async def unbind_teacher_from_subject(data: dict, session: AsyncSession) -> bool:
        query = (
            select(subject_teacher_association)
            .where(
                subject_teacher_association.c.subject_id == data["subject_id"],
                subject_teacher_association.c.teacher_id == data["teacher_id"],
            )
        )

        result = await session.execute(query)
        exists = result.first()

        if not exists:
            return False

        stmt = (
            delete(subject_teacher_association)
            .where(
                subject_teacher_association.c.subject_id == data["subject_id"],
                subject_teacher_association.c.teacher_id == data["teacher_id"],
            )
        )

        await session.execute(stmt)
        await session.flush()

        return True