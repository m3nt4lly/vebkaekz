from datetime import datetime, time
from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    student_id: int
    teacher_id: int
    day_of_week: str = Field(min_length=2, max_length=20)
    start_time: time
    end_time: time
    room: str = Field(min_length=1, max_length=50)


class ScheduleUpdate(BaseModel):
    student_id: int | None = None
    teacher_id: int | None = None
    day_of_week: str | None = Field(None, min_length=2, max_length=20)
    start_time: time | None = None
    end_time: time | None = None
    room: str | None = Field(None, min_length=1, max_length=50)


class ScheduleResponse(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    student_name: str | None = None
    teacher_name: str | None = None
    day_of_week: str
    start_time: time
    end_time: time
    room: str
    created_at: datetime
    model_config = {"from_attributes": True}
