from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from ..database.models.group_model import Group
from ..database.models.student_model import Student


class GroupRepository:
    @staticmethod
    async def create_group(data: dict, session: AsyncSession) -> Group:
        group = Group(**data)
        session.add(group)
        await session.flush()
        return group
    
    @staticmethod
    async def delete_group(group_id: int, session: AsyncSession) -> None:
        await session.execute(
            update(Student)
            .where(Student.group_id == group_id)
            .values(group_id=None)
        )
        
        await session.execute(
            delete(Group).where(Group.id == group_id)
        )
    
    @staticmethod
    async def get_all_groups(session: AsyncSession) -> list[Group]:
        result = await session.execute(
            select(Group)
            .options(joinedload(Group.students))
        )
        return result.unique().scalars().all()