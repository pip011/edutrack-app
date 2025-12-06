from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models.subject_model import Subject
from ..database.models.teacher_model import Teacher


class SubjectRepository:
    @staticmethod
    async def add_subject(data: dict, session: AsyncSession) -> Subject:
        subject = Subject(**data)
        session.add(subject)
        await session.flush()
        return subject
    
    @staticmethod
    async def delete_subject(subject_id: int, session: AsyncSession) -> int | None:
        result = await session.execute(
            delete(Subject).where(Subject.id == subject_id)
            .returning(Subject.id)
        )
        
        deleted_id = result.scalar()
        return deleted_id
    
    @staticmethod
    async def get_subject_by_id(subject_id: int, session: AsyncSession) -> Subject:
        result = await session.execute(
            select(Subject).where(Subject.id == subject_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_subjects(session: AsyncSession) -> list[Subject]:
        result = await session.execute(
            select(Subject)
            .options(
                joinedload(Subject.teachers)
            )
        )
        return result.unique().scalars().all()
    
    @staticmethod
    async def get_subjects_for_teacher(teacher_id: int, session: AsyncSession):
        stmt = (
            select(Subject)
            .options(joinedload(Subject.teachers))
            .join(Subject.teachers)
            .where(Teacher.id == teacher_id)
        )
        result = await session.execute(stmt)
        return result.unique().scalars().all()