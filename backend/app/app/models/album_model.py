from app.models.user_model import User
from sqlmodel import Field, Relationship, SQLModel
from app.models.base_uuid_model import BaseUUIDModel
from uuid import UUID



class AlbumBase(SQLModel):
    album_name: str = Field(index=True)
    artist: str


class Album(BaseUUIDModel, AlbumBase, table=True):
    tracks: list["Track"] = Relationship( 
        back_populates="album",  sa_relationship_kwargs={"lazy": "selectin"}
    )


    created_by_id: UUID | None = Field(default=None, foreign_key="User.id")
    created_by: User | None = Relationship( 
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Album.created_by_id==User.id",
        }
    )
