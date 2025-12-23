from datetime import date
from sqlalchemy import select, func, or_
from backend.app.data.db import get_session
from backend.app.data.db_requests.base import BaseRequests


class StudentRequests(BaseRequests):

    async def get_by_id(self, student_id: int):
        async with get_session() as session:
            return await session.scalar(
                select(self.Student).where(self.Student.id == student_id)
            )

    async def get_by_email(self, email: str):
        async with get_session() as session:
            return await session.scalar(
                select(self.Student).where(self.Student.email == email)
            )

    async def get_list(self, page: int = 1, per_page: int = 10, search: str | None = None):
        async with get_session() as session:
            query = select(self.Student)
            count_query = select(func.count(self.Student.id))

            if search:
                search_filter = or_(
                    self.Student.first_name.ilike(f"%{search}%"),
                    self.Student.last_name.ilike(f"%{search}%"),
                    self.Student.email.ilike(f"%{search}%"),
                    self.Student.phone.ilike(f"%{search}%"),
                )
                query = query.where(search_filter)
                count_query = count_query.where(search_filter)

            total = await session.scalar(count_query)
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page).order_by(self.Student.id)
            result = await session.scalars(query)
            return result.all(), total or 0

    async def create(self, first_name: str, last_name: str, email: str, phone: str, birth_date: date):
        async with get_session() as session:
            student = self.Student(
                first_name=first_name, last_name=last_name,
                email=email, phone=phone, birth_date=birth_date
            )
            session.add(student)
            await session.flush()
            await session.refresh(student)
            return student

    async def update(self, student_id: int, first_name: str | None = None, last_name: str | None = None,
                     email: str | None = None, phone: str | None = None, birth_date: date | None = None):
        async with get_session() as session:
            student = await session.scalar(select(self.Student).where(self.Student.id == student_id))
            if not student:
                return None
            if first_name: student.first_name = first_name
            if last_name: student.last_name = last_name
            if email: student.email = email
            if phone: student.phone = phone
            if birth_date: student.birth_date = birth_date
            await session.flush()
            await session.refresh(student)
            return student

    async def delete(self, student_id: int) -> bool:
        async with get_session() as session:
            student = await session.scalar(select(self.Student).where(self.Student.id == student_id))
            if not student:
                return False
            await session.delete(student)
            return True


student_requests = StudentRequests()
