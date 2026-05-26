from fastapi import HTTPException
from shared.entities.song import Song
from .repository import SongRepository

class SongService:
    def __init__(self, repo: SongRepository):
        self.repo = repo

    async def create(
        self,
        title: str,
        album_id: str,
        artist_id: str,              
        feat_ids: list[str] | None = None,
        duration_sec: int | None = None,
    ) -> Song:

        artists_db = await self.repo.get_artists_by_ids([artist_id])
        if not artists_db:
            raise HTTPException(status_code=404, detail="Main artist not found")

        if feat_ids:
            if artist_id in feat_ids:
                raise HTTPException(
                    status_code=400,
                    detail="Main artist cannot be also in feats"
                )

            feat_artists = await self.repo.get_artists_by_ids(feat_ids)
            if len(feat_artists) != len(feat_ids):
                raise HTTPException(status_code=404, detail="One or more feat artists not found")

        if duration_sec is not None and duration_sec <= 0:
            raise HTTPException(status_code=400, detail="Duration must be greater than 0")

        song = Song(
            title=title,
            album_id=album_id,
            artist_id=artist_id,
            duration_sec=duration_sec,
        )
        # Adicionar feats
        if feat_ids:
            for artist in await self.repo.get_artists_by_ids(feat_ids):
                song.feats.append(artist)

        return await self.repo.save(song)

    async def get_all(self, album_id: str | None = None) -> list[Song]:
        return await self.repo.get_all(album_id)

    async def get_by_id(self, song_id: str) -> Song:
        song = await self.repo.get_by_id(song_id)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
        return song

    async def update(
        self,
        song_id: str,
        title: str | None = None,
        duration_sec: int | None = None,
        artist_id: str | None = None,
        feat_ids: list[str] | None = None,
    ) -> Song:
        song = await self.get_by_id(song_id)

        if title is not None:
            song.title = title
        if duration_sec is not None:
            if duration_sec <= 0:
                raise HTTPException(status_code=400, detail="Duration must be greater than 0")
            song.duration_sec = duration_sec

        if artist_id is not None:
            artist_db = await self.repo.get_artists_by_ids([artist_id])
            if not artist_db:
                raise HTTPException(status_code=404, detail="Main artist not found")

            song.artist_id = artist_id

        if feat_ids is not None:
            
            current_artist_id = artist_id if artist_id is not None else song.artist_id
            if current_artist_id in feat_ids:
                raise HTTPException(
                    status_code=400,
                    detail="Main artist cannot be also in feats"
                )

            feat_artists = await self.repo.get_artists_by_ids(feat_ids)
            if len(feat_artists) != len(feat_ids):
                raise HTTPException(status_code=404, detail="One or more feat artists not found")
            
            song.feats.clear()
            for artist in feat_artists:
                song.feats.append(artist)

        return await self.repo.save(song)

    async def delete(self, song_id: str) -> None:
        song = await self.get_by_id(song_id)
        await self.repo.delete(song)