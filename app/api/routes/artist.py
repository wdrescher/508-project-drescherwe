from fastapi import APIRouter, HTTPException, Depends
from typing import List

from api.models.user import Profile, Artist, ArtistProfileList
from api.models.parlor import Parlor
from api.models.responses import SuccessResponse
from api.services import artist
from api.services.dependencies import get_current_user, get_artist, get_current_artist

router = APIRouter(
    prefix="/artist", 
    tags=["Artist"]
)

@router.post("/create")
async def create_artist_endpoint(request: Artist, current_user: Profile = Depends(get_current_user)): 
    artist_exists = await get_artist(current_user.profile_id)
    if artist_exists is not None: 
        return SuccessResponse()
    response = await artist.create_artist(current_user, request)
    if response is None: 
        raise HTTPException(status_code=301)
    return SuccessResponse()

@router.get("", response_model=Artist)
async def get_current_artist(current_artist: Artist = Depends(get_current_artist)):
    return current_artist

@router.get("/list", response_model=ArtistProfileList)
async def get_artists_endpoint(): 
    artists = await artist.get_artists()
    return ArtistProfileList.parse_obj(artists)

@router.get("/{artist_id}", response_model=Artist)
async def get_artist_from_id(artist_id: str): 
    artist = await get_artist(artist_id)
    if artist is None: 
        raise HTTPException(status_code=404, detail="No artist found")
    return Artist(**dict(artist))