from pydantic import BaseModel

class Booking(BaseModel): 
    artist_id: int
    client_id: int
    booking_id: int
    design_description: str
    design_approved: bool
    price: int
    price_approved: bool

class Timeslot(BaseModel): 
    date_time: str
    booking_id: str