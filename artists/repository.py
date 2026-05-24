from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from shared.entities.artist import Artist

class ArtistRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Artist]:
        result = await self.session.execute(select(Artist))
        return result.scalars().all()

    async def get_by_id(self, artist_id: str) -> Artist | None:
        return await self.session.get(Artist, artist_id)

    async def get_by_name(self, name: str) -> Artist | None:
        stmt = select(Artist).where(Artist.name.ilike(name))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, artist: Artist) -> Artist:
        self.session.add(artist)
        await self.session.commit()
        await self.session.refresh(artist)
        return artist

    async def delete(self, artist: Artist) -> None:
        await self.session.delete(artist)
        await self.session.commit()