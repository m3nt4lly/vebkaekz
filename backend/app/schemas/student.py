from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field


class StudentCreate(BaseModel):
    first_name: str = Field(min_length=2, max_length=100)
    last_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(pattern=r'^\+?[0-9]{10,15}$')
    birth_date: date


class StudentUpdate(BaseModel):
    first_name: str | None = Field(None, min_length=2, max_length=100)
    last_name: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, pattern=r'^\+?[0-9]{10,15}$')
    birth_date: date | None = None


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    birth_date: date
    created_at: datetime
    model_config = {"from_attributes": True}
