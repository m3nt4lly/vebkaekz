from sqlalchemy import select, func, or_
from backend.app.data.db import get_session
from backend.app.data.db_requests.base import BaseRequests


class InstrumentRequests(BaseRequests):

    async def get_by_id(self, instrument_id: int):
        async with get_session() as session:
            return await session.scalar(
                select(self.Instrument).where(self.Instrument.id == instrument_id)
            )

    async def get_list(self, page: int = 1, per_page: int = 10, search: str | None = None):
        async with get_session() as session:
            query = select(self.Instrument)
            count_query = select(func.count(self.Instrument.id))

            if search:
                search_filter = or_(
                    self.Instrument.name.ilike(f"%{search}%"),
                    self.Instrument.type.ilike(f"%{search}%"),
                    self.Instrument.brand.ilike(f"%{search}%"),
                    self.Instrument.condition.ilike(f"%{search}%"),
                )
                query = query.where(search_filter)
                count_query = count_query.where(search_filter)

            total = await session.scalar(count_query)
            offset = (page - 1) * per_page
            query = query.offset(offset).limit(per_page).order_by(self.Instrument.id)
            result = await session.scalars(query)
            return result.all(), total or 0

    async def create(self, name: str, type: str, brand: str, condition: str):
        async with get_session() as session:
            instrument = self.Instrument(name=name, type=type, brand=brand, condition=condition)
            session.add(instrument)
            await session.flush()
            await session.refresh(instrument)
            return instrument

    async def update(self, instrument_id: int, name: str | None = None, type: str | None = None,
                     brand: str | None = None, condition: str | None = None):
        async with get_session() as session:
            instrument = await session.scalar(select(self.Instrument).where(self.Instrument.id == instrument_id))
            if not instrument:
                return None
            if name: instrument.name = name
            if type: instrument.type = type
            if brand: instrument.brand = brand
            if condition: instrument.condition = condition
            await session.flush()
            await session.refresh(instrument)
            return instrument

    async def delete(self, instrument_id: int) -> bool:
        async with get_session() as session:
            instrument = await session.scalar(select(self.Instrument).where(self.Instrument.id == instrument_id))
            if not instrument:
                return False
            await session.delete(instrument)
            return True


instrument_requests = InstrumentRequests()
