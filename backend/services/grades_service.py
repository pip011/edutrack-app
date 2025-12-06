from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.grade_repository import GradeRepository
from ..schemas.grade_schema import Grade, GradesList, GradesForSubject, CreateGrade, GradeUpdate

class GradeService():
    @staticmethod
    async def get_grades_for_subject(data: GradesForSubject, session: AsyncSession):
        grades = await GradeRepository.get_grades_for_subject(subject_id=data.subject_id,
                                                        month=data.month, 
                                                        year=data.year, 
                                                        session=session)
        result = [Grade.model_validate(g) for g in grades]
        return GradesList(grades=result)
    
    @staticmethod
    async def add_grade(data: CreateGrade, session: AsyncSession) -> Grade:
        grade = await GradeRepository.add_grade(data.model_dump(), session)
        return Grade.model_validate(grade)
    
    @staticmethod 
    async def delete_grade(grade_id: int, session: AsyncSession) -> int | None:
        result = await GradeRepository.delete_grade(grade_id, session)
        return result
    
    @staticmethod 
    async def update_grade(grade_id: int, data: GradeUpdate, session: AsyncSession):
        grade = await GradeRepository.update(grade_id, data.model_dump(), session)
        return grade