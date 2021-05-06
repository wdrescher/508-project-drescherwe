from fastapi import APIRouter, Depends

from api.models.parlor import Parlor
from api.models.requests import CreateParlorRequest
from api.services.parlor import get_parlor, create_parlor
from api.services.dependencies import get_current_artist, get_current_user
from api.services.artist import set_parlor

router = APIRouter(
    prefix="/parlor", 
    tags=["Parlor"]
)

@router.get("/{parlor_id}", response_model=Parlor)
async def get_parlor_endpoint(parlor_id: str): 
    parlor = await get_parlor(parlor_id)
    return parlor

@router.post("/create", response_model=Parlor)
async def create_parlor_endpoint(request: CreateParlorRequest, current_artist = Depends(get_current_artist), current_user = Depends(get_current_user)):
    parlor = await create_parlor(request)
    await set_parlor(current_user, parlor.parlor_id)
    return parlor

