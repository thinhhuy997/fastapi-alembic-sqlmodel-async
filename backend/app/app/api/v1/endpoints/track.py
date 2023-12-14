from uuid import UUID
from app.api.celery_task import print_hero
from app.utils.exceptions import IdNotFoundException, NameNotFoundException
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.models.track_model import Track
from app.models.user_model import User
from app.schemas.common_schema import IOrderEnum
from app.schemas.track_schema import (
    ITrackCreate,
    ITrackRead,
    ITrackReadWithAlbum,
    ITrackUpdate
)
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase,
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)

from app.schemas.role_schema import IRoleEnum
from app.core.authz import is_authorized

router = APIRouter()

@router.get("")
async def get_track_list(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[ITrackReadWithAlbum]:
    """
    Gets a paginated list of tracks
    """
    tracks = await crud.track.get_multi_paginated(params=params)
    return create_response(data=tracks)

@router.get("/get_by_id/{track_id}")
async def get_track_by_id(
    track_id: UUID,
    current_user: User = Depends(deps.get_current_user())
) -> IGetResponseBase[ITrackReadWithAlbum]:
    """
    Gets a track by its id
    """
    track = await crud.track.get(id = track_id)
    if not track:
        raise IdNotFoundException(Track, track_id)
    
    return create_response(data=track)

@router.post("")
async def create_track(
    track: ITrackCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPostResponseBase[ITrackRead]:
    """
    Creates a new track

    Required roles:
    - admin
    - manager
    """
    created_track = await crud.track.create(obj_in=track, created_by_id=current_user.id)
    return create_response(data=created_track)

@router.delete("/{track_id}")
async def remove_track(
    track_id: UUID,
    current_user: User = Depends (
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    )
) -> IDeleteResponseBase[ITrackRead]:
    """
    Deletes a track by its id

    Required roles:
    - admin
    - manager
    """
    current_track = await crud.track.get(id = track_id)
    if not current_track:
        raise IdNotFoundException(Track, track_id)
    track = await crud.track.remove(id=track_id)
    return create_response(data=track)

@router.delete("/")
async def remove_all_tracks(
    current_user: User = Depends (
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    )
) -> IDeleteResponseBase[ITrackRead]:
    """
    Deletes a track by its id

    Required roles:
    - admin
    - manager
    """
    tracks = await crud.track.remove_all()
    return create_response(data={})