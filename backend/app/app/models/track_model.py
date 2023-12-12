from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID
from typing import Optional

class TrackBase(SQLModel):
    title: str = Field(index=True)
    order: int
    duration: int

class Track(BaseUUIDModel, TrackBase, table=True):
    album_id: Optional[int] = Field(default=None, foreign_key="album.id")
    album: "Album" = Relationship(
        back_populates="tracks"
    )

    created_by_id: UUID | None = Field(default=None, foreign_key="User.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Track.created_by_id==User.id",
        }
    )
