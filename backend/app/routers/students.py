import math
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from backend.app.data.models import User
from backend.app.data.db_requests.students import student_requests
from backend.app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from backend.app.schemas.common import PaginatedResponse
from backend.app.utils.security import get_current_user

router = APIRouter(prefix="/api/students", tags=["Ученики"])


@router.get("", response_model=PaginatedResponse[StudentResponse])
async def get_students(
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100),
    search: str | None = Query(None)
):
    items, total = await student_requests.get_list(page=page, per_page=per_page, search=search)
    return {"items": items, "total": total, "page": page, "per_page": per_page,
            "pages": math.ceil(total / per_page) if total > 0 else 1}


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    student = await student_requests.get_by_id(student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.post("", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(student_data: StudentCreate, current_user: Annotated[User, Depends(get_current_user)]):
    if await student_requests.get_by_email(student_data.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    return await student_requests.create(
        first_name=student_data.first_name, last_name=student_data.last_name,
        email=student_data.email, phone=student_data.phone, birth_date=student_data.birth_date
    )


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student_data: StudentUpdate,
                         current_user: Annotated[User, Depends(get_current_user)]):
    if student_data.email:
        existing = await student_requests.get_by_email(student_data.email)
        if existing and existing.id != student_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    student = await student_requests.update(
        student_id=student_id, first_name=student_data.first_name, last_name=student_data.last_name,
        email=student_data.email, phone=student_data.phone, birth_date=student_data.birth_date
    )
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    if not await student_requests.delete(student_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
