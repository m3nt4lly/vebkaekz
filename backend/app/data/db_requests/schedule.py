from datetime import time
from sqlalchemy import select, func, or_
from sqlalchemy.orm import selectinload
from backend.app.data.db import get_session
from backend.app.data.db_requests.base import BaseRequests


class ScheduleRequests(BaseRequests):

    async def get_by_id(self, schedule_id: int):
        async with get_session() as session:
            return await session.scalar(
                select(self.Schedule)
                .options(selectinload(self.Schedule.student), selectinload(self.Schedule.teacher))
                .where(self.Schedule.id == schedule_id)
            )

    async def get_list(self, page: int = 1, per_page: int = 10, search: str | None = None):
        async with get_session() as session:
            query = select(self.Schedule).options(
                selectinload(self.Schedule.student), selectinload(self.Schedule.teacher)
            )
            count_query = select(func.count(self.Schedule.id))

            if search:
                query = query.join(self.Schedule.student).join(self.Schedule.teacher)
                count_query = count_query.select_from(self.Schedule).join(self.Schedule.student).join(self.Schedule.teacher)
                search_filter = or_(
                    self.Schedule.day_of_week.ilike(f"%{search}%"),
                    self.Schedule.room.ilike(f"%{search}%"),
                    self.Student.first_name.ilike(f"%{search}%"),
                    self.Student.last_name.ilike(f"%{search}%"),
                    self.Teacher.first_name.ilike(f"%{search}%"),
                    self.Teacher.last_name.ilike(f"%{search}%"),
                )
                query = query.where(search_filter)
                count_query = count_query.where(search_filter)

            total = await session.scalar(count_query)
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page).order_by(self.Schedule.id)
            result = await session.scalars(query)
            return result.all(), total or 0

    async def create(self, student_id: int, teacher_id: int, day_of_week: str,
                     start_time: time, end_time: time, room: str):
        async with get_session() as session:
            schedule = self.Schedule(
                student_id=student_id, teacher_id=teacher_id, day_of_week=day_of_week,
                start_time=start_time, end_time=end_time, room=room
            )
            session.add(schedule)
            await session.flush()
            return await session.scalar(
                select(self.Schedule)
                .options(selectinload(self.Schedule.student), selectinload(self.Schedule.teacher))
                .where(self.Schedule.id == schedule.id)
            )

    async def update(self, schedule_id: int, student_id: int | None = None, teacher_id: int | None = None,
                     day_of_week: str | None = None, start_time: time | None = None,
                     end_time: time | None = None, room: str | None = None):
        async with get_session() as session:
            schedule = await session.scalar(select(self.Schedule).where(self.Schedule.id == schedule_id))
            if not schedule:
                return None
            if student_id: schedule.student_id = student_id
            if teacher_id: schedule.teacher_id = teacher_id
            if day_of_week: schedule.day_of_week = day_of_week
            if start_time: schedule.start_time = start_time
            if end_time: schedule.end_time = end_time
            if room: schedule.room = room
            await session.flush()
            return await session.scalar(
                select(self.Schedule)
                .options(selectinload(self.Schedule.student), selectinload(self.Schedule.teacher))
                .where(self.Schedule.id == schedule.id)
            )

    async def delete(self, schedule_id: int) -> bool:
        async with get_session() as session:
            schedule = await session.scalar(select(self.Schedule).where(self.Schedule.id == schedule_id))
            if not schedule:
                return False
            await session.delete(schedule)
            return True


schedule_requests = ScheduleRequests()
