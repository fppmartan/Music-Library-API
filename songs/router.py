from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from shared.db.session import AsyncSessionFactory
from .repository import SongRepository
from .service import SongService

router = APIRouter(prefix="/songs", tags=["Songs"])

async def get_session():
    async with AsyncSessionFactory() as session:
        yield session

@router.get("/", status_code=status.HTTP_200_OK)
async def list_songs(
    album_id: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    repo = SongRepository(session)
    service = SongService(repo)
    return await service.get_all(album_id)

@router.get("/{song_id}", status_code=status.HTTP_200_OK)
async def get_song(song_id: str, session: AsyncSession = Depends(get_session)):
    repo = SongRepository(session)
    service = SongService(repo)
    return await service.get_by_id(song_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_song(
    title: str = Query(...),
    album_id: str = Query(...),
    artist_id: str = Query(...),
    feat_ids: Optional[str] = Query(None, description="IDs dos feats separados por vírgula"),
    duration_sec: Optional[int] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    feat_ids_list = feat_ids.split(",") if feat_ids else []
    repo = SongRepository(session)
    service = SongService(repo)
    return await service.create(
        title=title,
        album_id=album_id,
        artist_id=artist_id,
        feat_ids=feat_ids_list,
        duration_sec=duration_sec,
    )

@router.put("/{song_id}", status_code=status.HTTP_200_OK)
async def update_song(
    song_id: str,
    title: Optional[str] = Query(None),
    duration_sec: Optional[int] = Query(None),
    artist_id: Optional[str] = Query(None),
    feat_ids: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    feat_ids_list = feat_ids.split(",") if feat_ids else None
    repo = SongRepository(session)
    service = SongService(repo)
    return await service.update(
        song_id=song_id,
        title=title,
        duration_sec=duration_sec,
        artist_id=artist_id,
        feat_ids=feat_ids_list,
    )

@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(song_id: str, session: AsyncSession = Depends(get_session)):
    repo = SongRepository(session)
    service = SongService(repo)
    await service.delete(song_id)