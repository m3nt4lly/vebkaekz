import math
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from backend.app.data.models import User
from backend.app.data.db_requests.schedule import schedule_requests
from backend.app.data.db_requests.students import student_requests
from backend.app.data.db_requests.teachers import teacher_requests
from backend.app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from backend.app.schemas.common import PaginatedResponse
from backend.app.utils.security import get_current_user

router = APIRouter(prefix="/api/schedule", tags=["Расписание"])


def _build_response(s):
    return {
        "id": s.id, "student_id": s.student_id, "teacher_id": s.teacher_id,
        "student_name": f"{s.student.first_name} {s.student.last_name}" if s.student else None,
        "teacher_name": f"{s.teacher.first_name} {s.teacher.last_name}" if s.teacher else None,
        "day_of_week": s.day_of_week, "start_time": s.start_time, "end_time": s.end_time,
        "room": s.room, "created_at": s.created_at
    }


@router.get("", response_model=PaginatedResponse[ScheduleResponse])
async def get_schedule_list(
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100),
    search: str | None = Query(None)
):
    items, total = await schedule_requests.get_list(page=page, per_page=per_page, search=search)
    return {"items": [_build_response(i) for i in items], "total": total, "page": page,
            "per_page": per_page, "pages": math.ceil(total / per_page) if total > 0 else 1}


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    schedule = await schedule_requests.get_by_id(schedule_id)
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return _build_response(schedule)


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(schedule_data: ScheduleCreate, current_user: Annotated[User, Depends(get_current_user)]):
    if not await student_requests.get_by_id(schedule_data.student_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not found")
    if not await teacher_requests.get_by_id(schedule_data.teacher_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher not found")
    schedule = await schedule_requests.create(
        student_id=schedule_data.student_id, teacher_id=schedule_data.teacher_id,
        day_of_week=schedule_data.day_of_week, start_time=schedule_data.start_time,
        end_time=schedule_data.end_time, room=schedule_data.room
    )
    return _build_response(schedule)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: int, schedule_data: ScheduleUpdate,
                          current_user: Annotated[User, Depends(get_current_user)]):
    if schedule_data.student_id and not await student_requests.get_by_id(schedule_data.student_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student not found")
    if schedule_data.teacher_id and not await teacher_requests.get_by_id(schedule_data.teacher_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teacher not found")
    schedule = await schedule_requests.update(
        schedule_id=schedule_id, student_id=schedule_data.student_id, teacher_id=schedule_data.teacher_id,
        day_of_week=schedule_data.day_of_week, start_time=schedule_data.start_time,
        end_time=schedule_data.end_time, room=schedule_data.room
    )
    if not schedule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return _build_response(schedule)


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(schedule_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    if not await schedule_requests.delete(schedule_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
