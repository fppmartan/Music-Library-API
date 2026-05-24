from datetime import datetime
from fastapi import HTTPException
from shared.entities.album import Album
from .repository import AlbumRepository

class AlbumService:
    def __init__(self, repo: AlbumRepository):
        self.repo = repo

    async def create(self, title: str, year: int, artist_id: str, cover_url: str | None = None) -> Album:
        # Validação: ano entre 1900 e ano atual
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            raise HTTPException(status_code=400, detail=f"Year must be between 1900 and {current_year}")

        # Validação: título único por artista
        existing = await self.repo.get_by_title_and_artist(title, artist_id)
        if existing:
            raise HTTPException(status_code=409, detail="Album with this title already exists for this artist")

        album = Album(title=title, year=year, artist_id=artist_id, cover_url=cover_url)
        return await self.repo.save(album)

    async def get_all(self) -> list[Album]:
        return await self.repo.get_all()

    async def get_by_id(self, album_id: str) -> Album:
        album = await self.repo.get_by_id(album_id)
        if not album:
            raise HTTPException(status_code=404, detail="Album not found")
        return album

    async def update(self, album_id: str, title: str | None, year: int | None, cover_url: str | None) -> Album:
        album = await self.get_by_id(album_id)

        if title is not None:
            # Se o título mudou, verifica unicidade por artista (ignorando o próprio álbum)
            existing = await self.repo.get_by_title_and_artist(title, album.artist_id)
            if existing and existing.id != album.id:
                raise HTTPException(status_code=409, detail="Album title already taken for this artist")
            album.title = title

        if year is not None:
            current_year = datetime.now().year
            if year < 1900 or year > current_year:
                raise HTTPException(status_code=400, detail=f"Year must be between 1900 and {current_year}")
            album.year = year

        if cover_url is not None:
            album.cover_url = cover_url

        return await self.repo.save(album)

    async def delete(self, album_id: str) -> None:
        album = await self.get_by_id(album_id)
        await self.repo.delete(album)