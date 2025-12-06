from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.group_schema import GroupsResponse, CreateGroup, Group, BindStudentToGroup, StudentId
from backend.schemas.student_schema import Student
from backend.services.groups_service import GroupService
from backend.services.authorization_service import AuthorizationService as Auth
from backend.database.db import get_session
from backend.enums import UserRole


router = APIRouter(prefix="/groups")

@router.get("/", response_model=GroupsResponse)
async def get_all_groups(_=Depends(Auth.require_role(UserRole.admin, UserRole.teacher)), session: AsyncSession = Depends(get_session)):
    groups = await GroupService.get_all_groups(session)
    return groups

@router.post("/", response_model=Group)
async def create_group(data: CreateGroup, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    group = await GroupService.create_group(data, session)
    await session.commit()
    return group

@router.post("/delete/{group_id}")
async def delete_group(group_id: int, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    await GroupService.delete_group(group_id, session)
    await session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/add-student/", response_model=Student)
async def add_student_to_group(data: BindStudentToGroup, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    student = await GroupService.bind_student_to_group(data, session)
    await session.commit()
    return student

@router.patch("/unbind-student", response_model=Student)
async def unbind_student_from_group(data: StudentId, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    student = await GroupService.unbind_student_from_group(data, session)
    await session.commit()
    return student