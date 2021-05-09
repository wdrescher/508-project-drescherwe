from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.services.dependencies import get_current_user, get_user_from_email
from api.models.user import Profile
from api.models.requests import AccessRequest, SignupRequest, ResetPasswordRequest, ChangePasswordRequest
from api.models.responses import TokenResponse, LoginResponse, SuccessResponse
from api.services.auth import create_user, check_password, change_password

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
    
@router.post("/change-password")
async def change_password_endpoint(request: ChangePasswordRequest, current_user: Profile = Depends(get_current_user)):
    result = await change_password(current_user, request.password)
    if result is None: 
        raise HTTPException(status_code=400, detail="Password not changed successfully")
    return SuccessResponse()