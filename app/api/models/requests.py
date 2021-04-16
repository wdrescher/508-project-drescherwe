from pydantic import BaseModel
from typing import List

from datetime import datetime

class SignupRequest(BaseModel): 
    email: str
    password: str
    first_name: str
    last_name: str

class AccessRequest(BaseModel): 
    email: str
    password: str

class ResetPasswordRequest(BaseModel): 
    profile_id: str
    new_password: str

class CreateBookingRequest(BaseModel): 
    artist_id: int
    design_description: str

class ScheduleBookingRequest(BaseModel): 
    times: List[datetime]