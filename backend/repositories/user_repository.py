from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models.user_model import User
from ..database.models.teacher_model import Teacher
from ..database.models.student_model import Student


class UserRepository():
    @classmethod
    async def create_user(cls, user_data: dict, session: AsyncSession) -> User:
        user = User(**user_data)
        session.add(user)
        await session.flush()
        return user
    
    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession) -> None:
        await session.execute(
            delete(Teacher).where(Teacher.user_id == user_id)
        )
        
        await session.execute(
            delete(Student).where(Student.user_id == user_id)
        )
        
        await session.execute(
            delete(User).where(User.id == user_id)
        )
        
        await session.flush()
    
    @classmethod
    async def find_user_by_username(cls, username: str, session: AsyncSession) -> User | None:
        result = await session.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[User]:
        result = await session.execute(
            select(User)
            .options(
                joinedload(User.student), 
                joinedload(User.teacher)
            )
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_by_user_id(user_id: int, session: AsyncSession) -> User:
        result = await session.execute(
            select(User).where(User.id == user_id)
            .options(
                joinedload(User.student), 
                joinedload(User.teacher)
            )
        )
        return result.scalar_one_or_none()
        
    @staticmethod
    async def update_user(
        user_id: int,
        user_data: dict | None,
        student_data: dict | None,
        teacher_data: dict | None, 
        session: AsyncSession) -> User:

        user = await UserRepository.get_by_user_id(user_id, session)
        if not user:
            return None
        
        if user_data:
            for field, value in user_data.items():
                setattr(user, field, value)

        if student_data:
            if user.student:
                for field, value in student_data.items():
                    setattr(user.student, field, value)

        if teacher_data:
            if user.teacher:
                for field, value in teacher_data.items():
                    setattr(user.teacher, field, value)
                    
        await session.refresh(user)

        return user