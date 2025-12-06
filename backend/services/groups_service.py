from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.group_schema import CreateGroup, Group, GroupsResponse, GroupWithStudents, BindStudentToGroup, StudentId
from ..schemas.student_schema import Student
from ..repositories.group_repository import GroupRepository
from ..repositories.student_repository import StudentRepository

class GroupService():
    @staticmethod
    async def create_group(data: CreateGroup, session: AsyncSession) -> Group:
        group = await GroupRepository.create_group(data.model_dump(), session)
        return Group.model_validate(group)
    
    @staticmethod
    async def delete_group(group_id: int, session: AsyncSession) -> None:
        await GroupRepository.delete_group(group_id, session=session)
        
    @staticmethod
    async def get_all_groups(session: AsyncSession) -> GroupsResponse:
        groups = await GroupRepository.get_all_groups(session)
        return GroupsResponse(groups=[GroupWithStudents.model_validate(g) for g in groups])
    
    @staticmethod
    async def bind_student_to_group(data: BindStudentToGroup, session: AsyncSession):
        student = await StudentRepository.update_student(student_id=data.student_id, data={'group_id': data.group_id}, session=session)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Студент с id '{data.student_id}' не найден" 
            )
        return Student.model_validate(student)
    
    @staticmethod 
    async def unbind_student_from_group(data: StudentId, session: AsyncSession):
        student = await StudentRepository.update_student(student_id=data.student_id, data={'group_id': None}, session=session)
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Студент с id '{data.student_id}' не найден")
        return Student.model_validate(student)
