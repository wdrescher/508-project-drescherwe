from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

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

class PaymentMethod(Enum): 
    TEXT = 'text'
    EMAIL = 'email'
    PHONE = 'phone'

class CreateClientRequest(BaseModel): 
    contact_method: Optional[PaymentMethod]
    payment_id: Optional[str]

class CreateParlorRequest(BaseModel): 
    name: str
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip: int
    shop_commission: float