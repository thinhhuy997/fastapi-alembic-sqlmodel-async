from app.models.track_model import TrackBase
from app.models.album_model import AlbumBase
from app.utils.partial import optional
from uuid import UUID
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel


class ITrackCreate(TrackBase):
    @field_validator('duration')
    def check_duration(cls, value):
        if value < 0:
            raise ValueError("Invalid duration")
        return value


# All these fields are optional
@optional()
class ITrackUpdate(TrackBase):
    pass


class ITrackRead(TrackBase):
    id: UUID


class ITrackReadWithAlbum(ITrackRead):
    album: AlbumBase | None

# New
class ITrackIds(SQLModel):
    list_ids: list[str]
