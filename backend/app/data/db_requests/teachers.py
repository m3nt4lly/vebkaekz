from sqlalchemy import select, func, or_
from backend.app.data.db import get_session
from backend.app.data.db_requests.base import BaseRequests


class TeacherRequests(BaseRequests):

    async def get_by_id(self, teacher_id: int):
        async with get_session() as session:
            return await session.scalar(
                select(self.Teacher).where(self.Teacher.id == teacher_id)
            )

    async def get_by_email(self, email: str):
        async with get_session() as session:
            return await session.scalar(
                select(self.Teacher).where(self.Teacher.email == email)
            )

    async def get_list(self, page: int = 1, per_page: int = 10, search: str | None = None):
        async with get_session() as session:
            query = select(self.Teacher)
            count_query = select(func.count(self.Teacher.id))

            if search:
                search_filter = or_(
                    self.Teacher.first_name.ilike(f"%{search}%"),
                    self.Teacher.last_name.ilike(f"%{search}%"),
                    self.Teacher.email.ilike(f"%{search}%"),
                    self.Teacher.phone.ilike(f"%{search}%"),
                    self.Teacher.specialization.ilike(f"%{search}%"),
                )
                query = query.where(search_filter)
                count_query = count_query.where(search_filter)

            total = await session.scalar(count_query)
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page).order_by(self.Teacher.id)
            result = await session.scalars(query)
            return result.all(), total or 0

    async def create(self, first_name: str, last_name: str, email: str, phone: str, specialization: str):
        async with get_session() as session:
            teacher = self.Teacher(
                first_name=first_name, last_name=last_name,
                email=email, phone=phone, specialization=specialization
            )
            session.add(teacher)
            await session.flush()
            await session.refresh(teacher)
            return teacher

    async def update(self, teacher_id: int, first_name: str | None = None, last_name: str | None = None,
                     email: str | None = None, phone: str | None = None, specialization: str | None = None):
        async with get_session() as session:
            teacher = await session.scalar(select(self.Teacher).where(self.Teacher.id == teacher_id))
            if not teacher:
                return None
            if first_name: teacher.first_name = first_name
            if last_name: teacher.last_name = last_name
            if email: teacher.email = email
            if phone: teacher.phone = phone
            if specialization: teacher.specialization = specialization
            await session.flush()
            await session.refresh(teacher)
            return teacher

    async def delete(self, teacher_id: int) -> bool:
        async with get_session() as session:
            teacher = await session.scalar(select(self.Teacher).where(self.Teacher.id == teacher_id))
            if not teacher:
                return False
            await session.delete(teacher)
            return True


teacher_requests = TeacherRequests()
