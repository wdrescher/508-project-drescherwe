from fastapi import APIRouter, Depends

from api.services.dependencies import get_current_user
from api.models.user import Profile
from api.models.requests import AccessRequest, SignupRequest
from api.models.responses import TokenResponse
from api.services.auth import create_user
router = APIRouter( 
    prefix="/auth"
)

@router.get("/test")
async def read_users_me(current_user: Profile = Depends(get_current_user)):
    return current_user

@router.post("/signup", response_model=TokenResponse)
async def singup(request: SignupRequest):
    token = await create_user(request)
    print(f"token: {token}")
    return token

@router.post("/login", response_model=Profile)
async def login(request: AccessRequest):
    return 
