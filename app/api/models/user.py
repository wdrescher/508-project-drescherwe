from typing import Optional

from pydantic import BaseModel

class Profile(BaseModel): 
    profile_id: int
    email: str
    phone_number: Optional[str]
    first_name: str
    last_name: str

class PrivateProfile(Profile): 
    password: str
    token_id: str

class Client(BaseModel): 
    payment_id: Optional[str]
    contact_method: Optional[str]

class Artist(BaseModel): 
    max_bookings: int
    is_manager: bool
    minimum_price: Optional[int] = None
    parlor_id: Optional[int] = None
