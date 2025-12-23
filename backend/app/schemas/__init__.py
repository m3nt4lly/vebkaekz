# Pydantic schemas module

from backend.app.schemas.common import PaginatedResponse
from backend.app.schemas.instrument import (
    InstrumentCreate,
    InstrumentResponse,
    InstrumentUpdate,
)
from backend.app.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse,
    ScheduleUpdate,
)
from backend.app.schemas.student import StudentCreate, StudentResponse, StudentUpdate
from backend.app.schemas.teacher import TeacherCreate, TeacherResponse, TeacherUpdate
from backend.app.schemas.user import Token, UserCreate, UserLogin, UserResponse

__all__ = [
    # User
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "Token",
    # Student
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    # Teacher
    "TeacherCreate",
    "TeacherUpdate",
    "TeacherResponse",
    # Instrument
    "InstrumentCreate",
    "InstrumentUpdate",
    "InstrumentResponse",
    # Schedule
    "ScheduleCreate",
    "ScheduleUpdate",
    "ScheduleResponse",
    # Common
    "PaginatedResponse",
]
