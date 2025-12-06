import bcrypt

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from ..database.db import new_session
from ..repositories.user_repository import UserRepository
from ..repositories.student_repository import StudentRepository
from ..repositories.teacher_repository import TeacherRepository
from ..schemas.user_schema import UserCreate, UserResponse, UserUpdate
from ..schemas.admin_schema import AdminUser, UsersResponse
from ..database.models.user_model import User
from ..enums import UserRole


class UserService:
    @staticmethod
    async def register_user(session: AsyncSession, user_data: UserCreate) -> User:
        existing_user = await UserRepository.find_user_by_username(username=user_data.username, session=session)
        if existing_user:
            raise ValueError("Пользователь с таким username уже существует")

        if user_data.role not in UserRole:
            raise ValueError(f"Недопустимая роль: {user_data.role}")

        password_bytes = user_data.password.encode('utf-8')
        password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        user_data.password = password_hash

        create_data = {
            "username": user_data.username,
            "password_hash": password_hash,
            "role": user_data.role
        }

        new_user = await UserRepository.create_user(user_data=create_data, session=session)
        
        match user_data.role:
            case 'student':
                await StudentRepository.create_student({'user_id': new_user.id}, session)
            case 'teacher':
                await TeacherRepository.create_teacher({'user_id': new_user.id}, session)

        return new_user
    
    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession) -> None:
        await UserRepository.delete_user(user_id, session)
    
    @staticmethod
    async def update_user(
        session: AsyncSession,
        user_id: int,
        update_data: UserUpdate) -> AdminUser:
        
        user_fields = None

        student_data = (
            update_data.student.model_dump(exclude_none=True)
            if update_data.student
            else None
        )
        
        teacher_data = (
            update_data.teacher.model_dump(exclude_none=True)
            if update_data.teacher
            else None
        )

        updated_user: User = await UserRepository.update_user(
            session=session,
            user_id=user_id,
            user_data=user_fields,
            student_data=student_data,
            teacher_data=teacher_data
        )
        
        return AdminUser.model_validate(updated_user)
        
    @staticmethod
    async def get_all_users(session: AsyncSession) -> UsersResponse:
        users: list[User] = await UserRepository.get_all_users(session)
        result = []
            
        for u in users:
            teacher = None
            student = None
            match u.role:
                case 'student':
                    if u.student:
                        student = u.student
                case 'teacher': 
                    if u.teacher:
                        teacher = u.teacher
            
            result.append(AdminUser(
                id=u.id, 
                role=u.role,
                username=u.username, 
                teacher=teacher, 
                student=student
            ))
            
        return UsersResponse(users=result)