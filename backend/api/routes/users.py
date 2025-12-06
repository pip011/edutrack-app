from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.models.teacher_model import Teacher
from backend.schemas.admin_schema import UsersResponse, AdminUser
from backend.schemas.teacher_schema import TeacherId, Teacher as STeacher
from backend.schemas.user_schema import UserUpdate
from backend.services.teachers_service import TeacherService
from backend.services.users_service import UserService
from backend.services.authorization_service import AuthorizationService as Auth
from backend.database.db import get_session
from backend.enums import UserRole


router = APIRouter(prefix="/users")

@router.get("/", response_model=UsersResponse)
async def get_all_users(_=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    users = await UserService.get_all_users(session)
    return users

@router.patch("/{user_id}", response_model=AdminUser)
async def update_user(user_id: int, data: UserUpdate, session: AsyncSession = Depends(get_session)):
    updated_user: AdminUser = await UserService.update_user(session, user_id, data)
    await session.commit()
    return updated_user

@router.post("/delete/{user_id}")
async def delete_user(user_id: int, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    await UserService.delete_user(user_id, session)
    await session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/teachers", response_model=STeacher)
async def get_teacher_by_user_id(user=Depends(Auth.require_role(UserRole.admin, UserRole.teacher)), session: AsyncSession = Depends(get_session)):
    teacher = await TeacherService.get_teacher_by_user_id(int(user['user_id']), session)
    if not teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Сущеость teacher для пользователя с id {user['user_id']} не найдена."
        )
    
    return teacher