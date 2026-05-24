from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from shared.entities.album import Album

class AlbumRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Album]:
        result = await self.session.execute(select(Album))
        return result.scalars().all()

    async def get_by_id(self, album_id: str) -> Album | None:
        return await self.session.get(Album, album_id)

    async def get_by_title_and_artist(self, title: str, artist_id: str) -> Album | None:
        stmt = select(Album).where(
            and_(Album.title.ilike(title), Album.artist_id == artist_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, album: Album) -> Album:
        self.session.add(album)
        await self.session.commit()
        await self.session.refresh(album)
        return album

    async def delete(self, album: Album) -> None:
        await self.session.delete(album)
        await self.session.commit()