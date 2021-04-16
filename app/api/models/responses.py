from pydantic import BaseModel
from datetime import date
from typing import List

from api.models.user import Profile
from api.models.booking import Booking

class TokenResponse(BaseModel): 
    bearer: str
    expiration_date: date

class LoginResponse(BaseModel): 
    profile: Profile
    token: str

class BookingListResponse(BaseModel): 
    bookings: List[Booking]

class SuccessResponse(BaseModel):
    """
    api -> client
    """

    status = 'ok'    