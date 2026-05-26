from fastapi import HTTPException
from shared.entities.artist import Artist
from .repository import ArtistRepository

class ArtistService:
    def __init__(self, repo: ArtistRepository):
        self.repo = repo

    async def create(self, name: str, country: str | None = None) -> Artist:
        existing = await self.repo.get_by_name(name)
        if existing:
            raise HTTPException(status_code=409, detail="Artist already exists")
        artist = Artist(name=name, country=country)
        return await self.repo.save(artist)

    async def get_all(self) -> list[Artist]:
        return await self.repo.get_all()

    async def get_by_id(self, artist_id: str) -> Artist:
        artist = await self.repo.get_by_id(artist_id)
        if not artist:
            raise HTTPException(status_code=404, detail="Artist not found")
        return artist

    async def update(self, artist_id: str, name: str | None, country: str | None) -> Artist:
        artist = await self.get_by_id(artist_id)
        if name is not None:
            existing = await self.repo.get_by_name(name)
            if existing and existing.id != artist.id:
                raise HTTPException(status_code=409, detail="Artist name already taken")
            artist.name = name
        if country is not None:
            artist.country = country
        return await self.repo.save(artist)

    async def delete(self, artist_id: str) -> None:
        artist = await self.get_by_id(artist_id)


        if await self.repo.has_songs_as_main(artist_id):
            raise HTTPException(
                status_code=409,
                detail="Artist cannot be deleted because they are the main artist in one or more songs"
            )

        if await self.repo.has_songs_as_feat(artist_id):
            raise HTTPException(
                status_code=409,
                detail="Artist cannot be deleted because they are featured in one or more songs"
            )

        await self.repo.delete(artist)