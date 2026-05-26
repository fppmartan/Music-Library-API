from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from shared.entities.song import Song
from shared.entities.artist import Artist

class SongRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, album_id: str | None = None) -> list[Song]:
        stmt = select(Song).options(selectinload(Song.artist), selectinload(Song.feats))
        if album_id:
            stmt = stmt.where(Song.album_id == album_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, song_id: str) -> Song | None:
        stmt = select(Song).where(Song.id == song_id).options(
            selectinload(Song.artist), selectinload(Song.feats)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, song: Song) -> Song:
        self.session.add(song)
        await self.session.commit()
        await self.session.refresh(song)
        await self.session.refresh(song, attribute_names=["artist", "feats"])
        return song

    async def delete(self, song: Song) -> None:
        await self.session.delete(song)
        await self.session.commit()

    async def get_artists_by_ids(self, artist_ids: list[str]) -> list[Artist]:
        stmt = select(Artist).where(Artist.id.in_(artist_ids))
        result = await self.session.execute(stmt)
        return result.scalars().all()