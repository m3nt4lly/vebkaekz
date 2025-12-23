import math
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from backend.app.data.models import User
from backend.app.data.db_requests.instruments import instrument_requests
from backend.app.schemas.instrument import InstrumentCreate, InstrumentUpdate, InstrumentResponse
from backend.app.schemas.common import PaginatedResponse
from backend.app.utils.security import get_current_user

router = APIRouter(prefix="/api/instruments", tags=["Инструменты"])


@router.get("", response_model=PaginatedResponse[InstrumentResponse])
async def get_instruments(
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=100),
    search: str | None = Query(None)
):
    items, total = await instrument_requests.get_list(page=page, per_page=per_page, search=search)
    return {"items": items, "total": total, "page": page, "per_page": per_page,
            "pages": math.ceil(total / per_page) if total > 0 else 1}


@router.get("/{instrument_id}", response_model=InstrumentResponse)
async def get_instrument(instrument_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    instrument = await instrument_requests.get_by_id(instrument_id)
    if not instrument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
    return instrument


@router.post("", response_model=InstrumentResponse, status_code=status.HTTP_201_CREATED)
async def create_instrument(instrument_data: InstrumentCreate, current_user: Annotated[User, Depends(get_current_user)]):
    return await instrument_requests.create(
        name=instrument_data.name, type=instrument_data.type,
        brand=instrument_data.brand, condition=instrument_data.condition
    )


@router.put("/{instrument_id}", response_model=InstrumentResponse)
async def update_instrument(instrument_id: int, instrument_data: InstrumentUpdate,
                            current_user: Annotated[User, Depends(get_current_user)]):
    instrument = await instrument_requests.update(
        instrument_id=instrument_id, name=instrument_data.name, type=instrument_data.type,
        brand=instrument_data.brand, condition=instrument_data.condition
    )
    if not instrument:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
    return instrument


@router.delete("/{instrument_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_instrument(instrument_id: int, current_user: Annotated[User, Depends(get_current_user)]):
    if not await instrument_requests.delete(instrument_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
