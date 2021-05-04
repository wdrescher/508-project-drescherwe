from fastapi import APIRouter, Depends, HTTPException

from api.services import auth
from api.services.dependencies import get_current_user, get_current_client
from api.models.user import Profile, Client
from api.models.requests import CreateClientRequest
from api.models.responses import SuccessResponse

router = APIRouter( 
    prefix="/user", 
    tags=["User"]
)

@router.get("/")
async def get_current_user(current_user: Profile = Depends(get_current_user)):
    return current_user

@router.post("/client")
async def create_client(request: CreateClientRequest, current_user: Profile = Depends(get_current_user)): 
    response = await auth.create_client(current_user, request)
    if not response: 
        raise HTTPException(status_code=301)
    return SuccessResponse()

@router.get("/client", response_model=Client)
async def get_client(current_client: Client = Depends(get_current_client)): 
    return current_client