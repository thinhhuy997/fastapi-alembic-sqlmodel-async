from typing import Any
from app.models.album_model import AlbumBase
from app.models.track_model import TrackBase
from .user_schema import IUserBasicInfo
from app.utils.partial import optional
from uuid import UUID


class IAlbumCreate(AlbumBase):
    pass


# All these fields are optional
@optional()
class IAlbumUpdate(AlbumBase):
    pass


class IAlbumRead(AlbumBase):
    id: UUID
    created_by: IUserBasicInfo


class IAlbumReadWithTrack(IAlbumRead):
    tracks: list[TrackBase]
