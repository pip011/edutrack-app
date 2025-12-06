from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.teacher_model import Teacher
from backend.database.models.user_model import User


class TeacherRepository:
    @staticmethod
    async def create_teacher(data: dict, session: AsyncSession):
        teacher = Teacher(**data)
        session.add(teacher)
        await session.flush()
        return teacher
    
    @staticmethod
    async def get_teacher_by_user_id(user_id: int, session: AsyncSession):
        stmt = (
        select(Teacher)
            .where(Teacher.user_id == user_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()