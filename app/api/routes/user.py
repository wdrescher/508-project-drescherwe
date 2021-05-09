from fastapi import APIRouter, Depends, HTTPException

from api.services import auth
from api.services.dependencies import get_current_user, get_current_client
from api.models.user import Profile, Client
from api.models.requests import CreateClientRequest, UpdateUserRequest
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

@router.post("/edit", response_model=Profile)
async def edit_current_user_endpoint(request: UpdateUserRequest, current_user: Profile = Depends(get_current_user)):
    result = await auth.edit_current_user(request, current_user)
    if result is None: 
        raise HTTPException(status_code=400, detail="failed to update user")
    current_user.first_name = request.first_name
    current_user.last_name = request.last_name
    return current_user