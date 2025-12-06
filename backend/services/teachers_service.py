from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.teacher_schema import Teacher
from ..schemas.user_schema import UserId
from ..repositories.teacher_repository import TeacherRepository


class TeacherService():
    @staticmethod 
    async def get_teacher_by_user_id(user_id: int, session: AsyncSession) -> Teacher | None:
        teacher = await TeacherRepository.get_teacher_by_user_id(user_id, session)
        if not teacher:
            return None
        
        return Teacher.model_validate(teacher)