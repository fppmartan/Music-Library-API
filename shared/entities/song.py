import uuid
from datetime import datetime
from sqlalchemy import Table, Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.db.base import Base
from shared.entities.artist import Artist  

song_feats = Table(
    "song_feats",
    Base.metadata,
    Column("song_id", ForeignKey("songs.id", ondelete="CASCADE"), primary_key=True),
    Column("artist_id", ForeignKey("artists.id", ondelete="CASCADE"), primary_key=True),
)

class Song(Base):
    __tablename__ = "songs"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    duration_sec: Mapped[int | None] = mapped_column(Integer, nullable=True)
    album_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("albums.id"), nullable=False)
    artist_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("artists.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    artist: Mapped[Artist] = relationship(Artist, foreign_keys=[artist_id])

    feats: Mapped[list[Artist]] = relationship(
        Artist, secondary=song_feats, backref="songs_as_feat"
    )