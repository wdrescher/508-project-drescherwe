from fastapi import APIRouter, Depends

from api.services.dependencies import get_current_user
from api.models.user import Profile

router = APIRouter( 
    prefix="/user"
)

@router.get("")
async def get_current_user(current_user: Profile = Depends(get_current_user)):
    return current_user