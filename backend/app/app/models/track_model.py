from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID
from typing import Optional

class TrackBase(SQLModel):
    title: str = Field(index=True)
    order: int
    duration: int | None = Field(default=None, index=True)
    album_id: UUID | None = Field(default=None, foreign_key="Album.id")

class Track(BaseUUIDModel, TrackBase, table=True):
    
    album: "Album" = Relationship(
        back_populates="tracks", sa_relationship_kwargs={"lazy": "joined"}
    )

    created_by_id: UUID | None = Field(default=None, foreign_key="User.id")
    created_by: "User" = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Track.created_by_id==User.id",
        }
    )
