from datetime import datetime
from sqlalchemy import extract, func, select, delete, text
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models.grade_model import Grade


class GradeRepository:
    @staticmethod
    async def add_grade(data: dict, session: AsyncSession) -> Grade:
        grade = Grade(**data)
        session.add(grade)
        await session.flush()
        return grade
    
    @staticmethod
    async def delete_grade(grade_id: int, session: AsyncSession) -> None:
        result = await session.execute(
            delete(Grade).where(Grade.id == grade_id)
            .returning(Grade.id)
        )
        
        return result.scalar()
    
    @staticmethod
    async def get_grade_by_id(grade_id: int, session: AsyncSession) -> Grade:
        result = await session.execute(
            select(Grade).where(Grade.id == grade_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def get_all_the_student_grades(student_id: int, session: AsyncSession) -> list[Grade]:
        result = await session.execute(
            select(Grade).where(Grade.student_id == student_id)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_grades_for_subject(subject_id: int, month: int, year: int, session: AsyncSession):
        start_date = f"{year:04d}-{month:02d}-01"
        
        start_date = f"{year:04d}-{month:02d}-01"
        end_date = f"{year:04d}-{month+1:02d}-01" if month < 12 else f"{year+1:04d}-01-01"

        stmt = text("""
            SELECT *
            FROM grades
            WHERE subject_id = :subject_id
              AND date >= :start_date
              AND date < :end_date
        """)
        
        result = await session.execute(stmt, {"subject_id": subject_id, "start_date": start_date, "end_date": end_date})
        rows = result.fetchall()
        return rows
    
    @staticmethod
    async def update(grade_id: int, data: dict, session: AsyncSession):
        grade = await GradeRepository.get_grade_by_id(grade_id, session)
        if not grade:
            return None
        
        for field, value in data.items():
            setattr(grade, field, value)
            
        await session.flush()
        return grade