from datetime import datetime, date, time

from sqlalchemy import String, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.data.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(20))
    birth_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    schedule_entries: Mapped[list["Schedule"]] = relationship(
        "Schedule", back_populates="student", cascade="all, delete-orphan"
    )


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    phone: Mapped[str] = mapped_column(String(20))
    specialization: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    schedule_entries: Mapped[list["Schedule"]] = relationship(
        "Schedule", back_populates="teacher", cascade="all, delete-orphan"
    )


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(50))
    brand: Mapped[str] = mapped_column(String(100))
    condition: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)


class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    day_of_week: Mapped[str] = mapped_column(String(20))
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    room: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="schedule_entries")
    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="schedule_entries")


class Models:
    User = User
    Student = Student
    Teacher = Teacher
    Instrument = Instrument
    Schedule = Schedule
