import uuid
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.db.base import Base

class Album(Base):
    __tablename__ = "albums"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    cover_url: Mapped[str | None] = mapped_column(String, nullable=True)
    artist_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("artists.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())