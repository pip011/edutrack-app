from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models.student_model import Student


class StudentRepository:
    @staticmethod
    async def create_student(data: dict, session: AsyncSession):
        student = Student(**data)
        session.add(student)
        await session.flush()
        return student
    
    @staticmethod
    async def update_student(student_id: int, data: dict, session: AsyncSession):
        result = await session.execute(
            select(Student).where(Student.id == student_id)
        )
        student = result.scalar_one_or_none()
        
        if not student:
            return None
        
        for field, value in data.items():
            if field in student.__table__.columns.keys():
                setattr(student, field, value)
                
        return student