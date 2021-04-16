from fastapi import APIRouter, Depends

from api.models.parlor import Parlor
from api.services.parlor import get_parlor, create_parlor
from api.services.dependencies import get_current_artist

router = APIRouter(
    prefix="/parlor", 
    tags=["Parlor"]
)

@router.get("/{parlor_id}", response_model=Parlor)
async def get_parlor_endpoint(parlor_id: str): 
    parlor = await get_parlor(parlor_id)
    return parlor

@router.post("/create", response_model=Parlor)
async def create_parlor_endpoint(request: Parlor, current_artist = Depends(get_current_artist)):
    parlor = await create_parlor(request)
    return parlor

