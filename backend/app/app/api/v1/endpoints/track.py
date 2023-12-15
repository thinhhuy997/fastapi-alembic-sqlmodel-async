from uuid import UUID
from app.api.celery_task import print_hero
from app.utils.exceptions import IdNotFoundException, NameNotFoundException
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Body
from fastapi_pagination import Params
from typing import Annotated
from app import crud
from app.api import deps
from app.models.track_model import Track
from app.models.album_model import Album
from app.models.user_model import User
from app.schemas.common_schema import IOrderEnum
from app.schemas.track_schema import (
    ITrackCreate,
    ITrackRead,
    ITrackReadWithAlbum,
    ITrackUpdate,
    ITrackIds
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
) -> IGetResponseBase[list[ITrackReadWithAlbum]]:
    """
    Gets a list of tracks
    """

    if current_user.is_superuser:
        tracks = await crud.track.get_multi()
    else:
        tracks = await crud.track.get_tracks_by_user_id(user_id=current_user.id)
    return create_response(data=tracks)

@router.post("/list-by-ids")
async def List_tracks_by_ids(
    list_ids: ITrackIds
) -> {}:
# IGetResponseBase[list[ITrackRead]]:
    """
    Gets a paginated list of tracks by list of ids
    """
    tracks = await crud.track.get_by_ids(list_ids=list_ids)

    return create_response(data = tracks)

@router.get("/list-track-by-album-id/{album_id}")
async def list_tracks_by_album_id(
    album_id: UUID,
) -> IGetResponseBase[list[ITrackReadWithAlbum]]:
    
    album = await crud.album.get(id=album_id)
   
    if not album:
        raise IdNotFoundException(Album, album_id)

    # function get_tracks_by_album_id is a custom function from track_crud.py
    tracks = await crud.track.get_tracks_by_album_id(album_id=album_id)
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
    if track.duration <= 0:
        raise HTTPException(
            status_code=400,
            detail= "Invalid Duration"
        )
    created_track = await crud.track.create(obj_in=track, created_by_id=current_user.id)
    return create_response(data=created_track)

@router.put("/{track_id}")
async def update_track(
    track_id: UUID,
    track_input: ITrackUpdate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    ),
) -> IPutResponseBase[ITrackRead]:
    """
    Updates a track by its id

    Required roles:
    - admin
    - manager
    """
    current_track = await crud.track.get(id=track_id)
    if not current_track:
        raise IdNotFoundException("Track", track_id)

    # Only the track owner can update their track
    if current_user.id != current_track.created_by_id:
        raise HTTPException(
            status_code=403,
            detail="You are not Authorized to update this track because you did not created it"
        )

    track_updated = await crud.hero.update(obj_new=track_input, obj_current=current_track)
    return create_response(data=track_updated)

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
        
    # if (not current_user.is_superuser) and (current_user.id != current_track.created_by_id):
    #     raise HTTPException(
    #         status_code=403,
    #         detail="You are not Authorized to delete this track because you did not created it"
    #     )

    """
    Admin can delete all tracks, but users can only delete tracks they own
    """
    if current_user.is_superuser or current_user.id == current_track.created_by_id:
        deleted_track = await crud.track.remove(id=track_id)
    else:
        raise HTTPException(
            status_code=403,
            detail="You are not Authorized to delete this track because you did not created it"
        )

    return create_response(data=deleted_track)

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


@router.get("/test-git")
async def test_git_or_something_like_that(

) -> {}:
    return create_response(data={})

