from app.schemas.track_schema import ITrackCreate, ITrackUpdate
from datetime import datetime
from app.crud.base_crud import CRUDBase
from app.models.track_model import Track
from sqlmodel import select, func, and_, col
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDTrack(CRUDBase[Track, ITrackCreate, ITrackUpdate]):
    # async def create(self, allbumId: str):
    #     album = albumCRUD.find_id(allbumId):
    #     if not album:

    #     super().create()


    async def get_track_by_name(
        self, *, name: str, db_session: AsyncSession | None = None
    ) -> Track:
        db_session = db_session or super().get_db().session
        track = await db_session.execute(
            select(Track).where(col(Track.title).ilike(f"%{name}%"))
        )
        return track.scalars().all()
    
    async def get_count_of_tracks(
        self,
        *,
        start_time: datetime,
        end_time: datetime,
        db_session: AsyncSession | None = None,
    ) -> int:
        db_session = db_session or super().get_db.session
        subquery = (
            select(Track)
            .where(
                and_(
                    Track.created_at > start_time,
                    Track.created_at < end_time,
                )
            )
            .subquery()
        )
        query = select(func.count()).select_from(subquery)
        count = await db_session.execute(query)
        value = count.scalar_one_or_none()
        return value
    

    # NEW
    async def get_tracks_by_album_id(
        self, *, album_id: str, db_session: AsyncSession | None = None
    ) -> Track:
        db_session = db_session or super().get_db().session
        track = await db_session.execute(
            select(Track).where(Track.album_id==album_id)
        )
        return track.scalars().all()

    # NEW
    async def get_tracks_by_user_id(
        self, user_id: str, *, db_session: AsyncSession | None = None
    ) -> Track:
        db_session = db_session or super().get_db().session
        tracks = await db_session.execute(
            select(Track).where(Track.created_by_id==user_id)
        )
        return tracks.scalars().all()
track = CRUDTrack(Track)