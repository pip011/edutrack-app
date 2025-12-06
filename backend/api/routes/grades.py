from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas.grade_schema import GradeUpdate, GradesList, GradesForSubject, CreateGrade, Grade
from backend.services.grades_service import GradeService
from backend.services.authorization_service import AuthorizationService as Auth
from backend.database.db import get_session
from backend.enums import UserRole


router = APIRouter(prefix="/grades")

@router.post("/sorted", response_model=GradesList)
async def get_grades_by_subject_and_year_with_month(data: GradesForSubject, _=Depends(Auth.require_role(UserRole.admin, UserRole.teacher)), session: AsyncSession = Depends(get_session)):
    result = await GradeService.get_grades_for_subject(data, session)
    return result

@router.post("/", response_model=Grade)
async def create_grade(data: CreateGrade,
                       _=Depends(Auth.require_role(UserRole.admin, UserRole.teacher)),
                       session: AsyncSession = Depends(get_session)):
    grade = await GradeService.add_grade(data, session)
    await session.commit()
    
    return grade

@router.post("/delete/{id}")
async def delete_grade(id: int, 
                       _=Depends(Auth.require_role(UserRole.admin, UserRole.teacher)),
                       session: AsyncSession = Depends(get_session)):
    deleted_grade_id = await GradeService.delete_grade(id, session)
    await session.commit()
    
    if deleted_grade_id is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Запись не найдена"
        )
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@router.patch("/grade/{id}", response_model=Grade)
async def update_grade(id: int, 
                       data: GradeUpdate,
                        _=Depends(Auth.require_role(UserRole.admin, UserRole.teacher)),
                        session: AsyncSession = Depends(get_session)):
    grade = await GradeService.update_grade(id, data, session)
    if not grade: 
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Оценка не найдена"
        )
    else: 
        await session.commit()
        return Grade.model_validate(grade)