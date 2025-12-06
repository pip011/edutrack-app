from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.db import get_session
from backend.services.authorization_service import AuthorizationService as Auth
from backend.enums import UserRole
from backend.schemas.subject_schema import Subject, AllSubjectsResponse, CreateSubject, BindSubjectTeacher
from backend.schemas.teacher_schema import TeacherId
from backend.services.subjects_service import SubjectService


router = APIRouter(prefix="/subjects")

@router.post("/", response_model=Subject)
async def create_subject(subject: CreateSubject, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    subject = await SubjectService.create_subject(subject, session)
    await session.commit()
    return subject

@router.get("/", response_model=AllSubjectsResponse)
async def get_all_subjects(_=Depends(Auth.require_role(UserRole.admin)), 
                           session: AsyncSession = Depends(get_session)):
    res = await SubjectService.get_all_subjects(session)
    return res

@router.post("/without-teachers", response_model=AllSubjectsResponse)
async def get_all_subjects_for_teacher(data: TeacherId, 
                                       _=Depends(Auth.require_role(UserRole.teacher)), 
                                        session: AsyncSession = Depends(get_session)):
    res = await SubjectService.get_all_subjects_for_teacher(data.id, session)
    return res

@router.post("/delete/{subject_id}")
async def delete_subject_by_id(subject_id: int, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    deleted_id = await SubjectService.delete_subject(subject_id, session)
    await session.commit()
    
    if deleted_id is None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмета с таким id не существует.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/bind-teacher")
async def bind_teacher_to_subject(data: BindSubjectTeacher, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    result = await SubjectService.bind_teacher_to_subject(data, session)
    
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Преподаватель уже привязан к этому предмету")
    
    await session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/unbind-teacher")
async def unbind_teacher_from_subject(data: BindSubjectTeacher, _=Depends(Auth.require_role(UserRole.admin)), session: AsyncSession = Depends(get_session)):
    result = await SubjectService.unbind_teacher_from_subject(data, session)
    
    if not result: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такой связи преподаватель-предмет не существует.")
    
    await session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)