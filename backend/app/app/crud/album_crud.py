from app.schemas.album_schema import IAlbumCreate, IAlbumUpdate
from app.crud.base_crud import CRUDBase
from app.models.album_model import Album
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDAlbum(CRUDBase[Album, IAlbumCreate, IAlbumUpdate]):
    # async def get_team_by_name(
    #     self, *, name: str, db_session: AsyncSession | None = None
    # ) -> Team:
    #     db_session = db_session or super().get_db().session
    #     team = await db_session.execute(select(Team).where(Team.name == name))
    #     return team.scalar_one_or_none()

    async def get_album_by_name(self, *, album_name: str, db_session: AsyncSession | None = None) -> Album:
        db_session = db_session or super().get_db().session
        album = await db_session.execute(select(Album).where(Album.album_name == album_name))
        return album.scalar_one_or_none()


album = CRUDAlbum(Album)
