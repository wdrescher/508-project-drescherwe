from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.services.dependencies import get_current_user, get_user_from_email
from api.models.user import Profile
from api.models.requests import AccessRequest, SignupRequest, ResetPasswordRequest
from api.models.responses import TokenResponse, LoginResponse
from api.services.auth import create_user, check_password

router = APIRouter( 
    prefix="/auth", 
    tags=["Auth"]
)

@router.post("/signup", response_model=TokenResponse)
async def singup(request: SignupRequest):
    token = await create_user(request)
    return token

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    profile = await check_password(username, password)
    if profile is None: 
        raise HTTPException(status_code=400, detail="Invalid username or password")
    else: 
        return {
            "access_token": profile.token_id, 
            "token_type": "bearer"
        }
    