import math
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from backend.app.data.models import User
from backend.app.data.db_requests.teachers import teacher_requests
from backend.app.schemas.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from backend.app.schemas.common import PaginatedResponse
from backend.app.utils.security import get_current_user

router = APIRouter(prefix="/api/teachers", tags=["Преподаватели"])


@router.get("", response_model=PaginatedResponse[TeacherResponse])
async def get_teachers(
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100),
    search: str | None = Query(None)
):
    items, total = await teacher_requests.get_list(page=page, per_page=per_page, search=search)
    return {"items": items, "total": total, "page": page, "per_page": per_page,
            "pages": math.ceil(total / per_page) if total > 0 else 1}


@router.get("/{teacher_id}", response_model=TeacherResponse)
async def get_teacher(teacher_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    teacher = await teacher_requests.get_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.post("", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(teacher_data: TeacherCreate, current_user: Annotated[User, Depends(get_current_user)]):
    if await teacher_requests.get_by_email(teacher_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    return await teacher_requests.create(
        first_name=teacher_data.first_name, last_name=teacher_data.last_name,
        email=teacher_data.email, phone=teacher_data.phone, specialization=teacher_data.specialization
    )


@router.put("/{teacher_id}", response_model=TeacherResponse)
async def update_teacher(teacher_id: int, teacher_data: TeacherUpdate,
                         current_user: Annotated[User, Depends(get_current_user)]):
    if teacher_data.email:
        existing = await teacher_requests.get_by_email(teacher_data.email)
        if existing and existing.id != teacher_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    teacher = await teacher_requests.update(
        teacher_id=teacher_id, first_name=teacher_data.first_name, last_name=teacher_data.last_name,
        email=teacher_data.email, phone=teacher_data.phone, specialization=teacher_data.specialization
    )
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(teacher_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    if not await teacher_requests.delete(teacher_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
