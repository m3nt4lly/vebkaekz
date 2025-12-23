from datetime import datetime
from pydantic import BaseModel, Field


class InstrumentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    type: str = Field(min_length=2, max_length=50)
    brand: str = Field(min_length=2, max_length=100)
    condition: str = Field(min_length=2, max_length=50)


class InstrumentUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    type: str | None = Field(None, min_length=2, max_length=50)
    brand: str | None = Field(None, min_length=2, max_length=100)
    condition: str | None = Field(None, min_length=2, max_length=50)


class InstrumentResponse(BaseModel):
    id: int
    name: str
    type: str
    brand: str
    condition: str
    created_at: datetime
    model_config = {"from_attributes": True}
