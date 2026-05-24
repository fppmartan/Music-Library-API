from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from shared.db.session import AsyncSessionFactory
from .repository import ArtistRepository
from .service import ArtistService

router = APIRouter(prefix="/artists", tags=["Artists"])

async def get_session():
    async with AsyncSessionFactory() as session:
        yield session

@router.get("/", status_code=status.HTTP_200_OK)
async def list_artists(session: AsyncSession = Depends(get_session)):
    repo = ArtistRepository(session)
    service = ArtistService(repo)
    return await service.get_all()

@router.get("/{artist_id}", status_code=status.HTTP_200_OK)
async def get_artist(artist_id: str, session: AsyncSession = Depends(get_session)):
    repo = ArtistRepository(session)
    service = ArtistService(repo)
    return await service.get_by_id(artist_id)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_artist(name: str, country: str | None = None, session: AsyncSession = Depends(get_session)):
    repo = ArtistRepository(session)
    service = ArtistService(repo)
    return await service.create(name, country)

@router.put("/{artist_id}", status_code=status.HTTP_200_OK)
async def update_artist(artist_id: str, name: str | None = None, country: str | None = None, session: AsyncSession = Depends(get_session)):
    repo = ArtistRepository(session)
    service = ArtistService(repo)
    return await service.update(artist_id, name, country)

@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(artist_id: str, session: AsyncSession = Depends(get_session)):
    repo = ArtistRepository(session)
    service = ArtistService(repo)
    await service.delete(artist_id)