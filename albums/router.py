from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.session import AsyncSessionFactory
from .repository import AlbumRepository
from .service import AlbumService

router = APIRouter(prefix="/albums", tags=["Albums"])

async def get_session():
    async with AsyncSessionFactory() as session:
        yield session

@router.get("/", status_code=status.HTTP_200_OK)
async def list_albums(session: AsyncSession = Depends(get_session)):
    repo = AlbumRepository(session)
    service = AlbumService(repo)
    return await service.get_all()

@router.get("/{album_id}", status_code=status.HTTP_200_OK)
async def get_album(album_id: str, session: AsyncSession = Depends(get_session)):
    repo = AlbumRepository(session)
    service = AlbumService(repo)
    return await service.get_by_id(album_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_album(
    title: str,
    year: int,
    artist_id: str,
    cover_url: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    repo = AlbumRepository(session)
    service = AlbumService(repo)
    return await service.create(title, year, artist_id, cover_url)

@router.put("/{album_id}", status_code=status.HTTP_200_OK)
async def update_album(
    album_id: str,
    title: str | None = None,
    year: int | None = None,
    cover_url: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    repo = AlbumRepository(session)
    service = AlbumService(repo)
    return await service.update(album_id, title, year, cover_url)

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_album(album_id: str, session: AsyncSession = Depends(get_session)):
    repo = AlbumRepository(session)
    service = AlbumService(repo)
    await service.delete(album_id)