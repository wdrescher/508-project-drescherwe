from pydantic import BaseModel
from datetime import date

from api.models.user import Profile

class TokenResponse(BaseModel): 
    bearer: str
    expiration_date: date

class LoginResponse(BaseModel): 
    profile: Profile
    token: str