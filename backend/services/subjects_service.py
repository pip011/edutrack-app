from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from ..repositories.subject_repository import SubjectRepository
from ..repositories.subject_teacher_repository import TeacherSubjectRepository
from ..schemas.subject_schema import Subject, CreateSubject, AllSubjectsResponse, SubjectWithTeachers, BindSubjectTeacher

class SubjectService():
    @staticmethod
    async def create_subject(subject: CreateSubject, session: AsyncSession) -> Subject:
        result = await SubjectRepository.add_subject(data=subject.model_dump(), session=session)
        return Subject.model_validate(result)
    
    @staticmethod 
    async def delete_subject(subject_id: int, session: AsyncSession) -> int | None:
        deleted_id = await SubjectRepository.delete_subject(subject_id, session)
        return deleted_id
        
    @staticmethod
    async def get_all_subjects(session: AsyncSession):
        subjects = await SubjectRepository.get_all_subjects(session)
        result = []
        
        for subject in subjects:
            result.append(SubjectWithTeachers.model_validate(subject))
        
        return AllSubjectsResponse(subjects=result)
    
    @staticmethod
    async def get_all_subjects_for_teacher(teacher_id: int, session: AsyncSession):
        subjects = await SubjectRepository.get_subjects_for_teacher(teacher_id, session)
        result = []
        
        for subject in subjects:
            result.append(SubjectWithTeachers.model_validate(subject))
        return AllSubjectsResponse(subjects=result)
    
    @staticmethod
    async def bind_teacher_to_subject(data: BindSubjectTeacher, session: AsyncSession) -> bool:
        try:
            result = await TeacherSubjectRepository.bind_teacher_to_subject(data.model_dump(), session)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Невозможно создать связь: subject_id или teacher_id не существует")
        return result
    
    @staticmethod
    async def unbind_teacher_from_subject(data: BindSubjectTeacher, session: AsyncSession) -> bool:
        result = await TeacherSubjectRepository.unbind_teacher_from_subject(data.model_dump(), session)
        return result