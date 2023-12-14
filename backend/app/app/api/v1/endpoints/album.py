from uuid import UUID
from app.utils.exceptions import (
    ContentNoChangeException,
    IdNotFoundException,
    NameExistException,
)
from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params
from app import crud
from app.api import deps
from app.models.album_model import Album
from app.models.user_model import User
from app.schemas.response_schema import (
    IDeleteResponseBase,
    IGetResponseBase, 
    IGetResponsePaginated,
    IPostResponseBase,
    IPutResponseBase,
    create_response,
)
from app.schemas.role_schema import IRoleEnum
from app.schemas.album_schema import (
    IAlbumCreate,
    IAlbumRead,
    IAlbumUpdate,
    IAlbumReadWithTrack
)

router = APIRouter()

@router.get("")
async def get_albums_list(
    params: Params = Depends(),
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponsePaginated[IAlbumReadWithTrack]:
    """
    Gets a paginated list of albums
    """
    albums = await crud.album.get_multi_paginated(params=params)
    print("albums", albums)
    return create_response(data=albums)

@router.get("/{album_id}")
async def get_album_by_id(
    album_id: UUID,
    current_user: User = Depends(deps.get_current_user()),
) -> IGetResponseBase[IAlbumRead]:
    """
    Gets a album by its id
    """
    album = await crud.album.get(id = album_id)
    if not album:
        raise IdNotFoundException(Album, id = album_id)
    return create_response(data=album)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_album(
    album: IAlbumCreate,
    current_user: User = Depends(
        deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])
    )
) -> IPostResponseBase[IAlbumRead]:
    """
    Creates a new team

    Required roles:
    - admin
    - manager
    """
    album_current = await crud.album.get_album_by_name(album_name=album.album_name)
    if album_current:
        raise NameExistException(Album, name=album_current.album_name)
    created_album = await crud.album.create(obj_in=album, created_by_id=current_user.id)
    return create_response(data=created_album)

@router.put("/{album_id}")
async def update_album(
    album_id: UUID,
    new_album: IAlbumUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager])),
) -> IPutResponseBase[IAlbumRead]:
    """
    Update a album by its id

    Required roles:
    - admin
    - manager
    """
    current_album = await crud.album.get(id = album_id)
    if not current_album:
        raise IdNotFoundException(Album, id = album_id)
    
    if (
        current_album.album_name == new_album.album_name
        and current_album.artist == new_album.artist
    ):
        raise ContentNoChangeException(detail="The content has not changed")
    
    exist_album = await crud.album.get_album_by_name(album_name=new_album.album_name)
    if exist_album:
        raise NameExistException(Album, name=exist_album.album_name)
    
    album_updated = await crud.album.update(obj_current = current_album,
                                                  obj_new=new_album)
    return create_response(data=album_updated)

@router.delete("/{album_id}")
async def remove_album(
    album_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin, IRoleEnum.manager]))
) -> IDeleteResponseBase[IAlbumRead]:
    """
    Deletes a album by its id

    Required roles:
    - admin
    - manager
    """
    current_album = await crud.album.get(id=album_id)
    if not current_album:
        raise IdNotFoundException(Album, id=album_id)
    album = await crud.album.remove(id=album_id)
    return create_response(data=album)
