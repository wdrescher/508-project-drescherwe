from db import database

from api.models.requests import CreateBookingRequest, ScheduleBookingRequest
from api.models.user import Profile
from api.models.booking import Booking

async def create_booking(request: CreateBookingRequest, current_user: Profile):
    async with database.connection():
        response = await database.execute(
            query="""
                    INSERT INTO booking (
                        artist_id, 
                        client_id,
                        design_description, 
                        design_approved, 
                        price, 
                        price_approved
                    ) 
                    VALUES (
                        :artist_id, 
                        :client_id, 
                        :design_description, 
                        FALSE,
                        0,
                        FALSE
                    );
            """,
            values={
                "artist_id": request.artist_id,
                "client_id": current_user.profile_id,
                "design_description": request.design_description,
            }
        )
        if response is None: 
            return None
        booking = await database.fetch_one(
            query="SELECT * FROM booking WHERE booking_id=(SELECT LAST_INSERT_ID())"
        )
    return booking

async def get_user_bookings(current_user: Profile): 
    async with database.connection(): 
        response = await database.fetch_all(
            query="""
                SELECT * FROM booking WHERE client_id=:profile_id
            """, 
            values={
                "profile_id": current_user.profile_id
            }
        )
    return response

async def set_price(current_user: Profile, booking_id: int, price: int):
    async with database.connection(): 
        response = await database.execute(
            query="""
                UPDATE booking SET price=:price, price_approved=False WHERE booking_id=:booking_id AND artist_id=:profile_id
            """, 
            values={
                "booking_id": booking_id, 
                "price": price,                 
                "profile_id": current_user.profile_id
            }
        )
    assert response is not None
    return response

async def approve_price(current_user: Profile, booking_id: int, approved=True): 
    async with database.connection(): 
        response = await database.execute(
            query="""
                UPDATE booking SET price_approved=:approved WHERE booking_id=:booking_id AND client_id=:profile_id
            """, 
            values={
                "booking_id": booking_id,
                "approved": approved, 
                "profile_id": current_user.profile_id
            }
        )
    return response

async def approve_design(current_user: Profile, booking_id: int, approved=True): 
    async with database.connection(): 
        response = await database.execute(
            query="""
                UPDATE booking SET design_approved=:approved WHERE booking_id=:booking_id AND artist_id=:profile_id
            """, 
            values={
                "booking_id": booking_id, 
                "approved": approved,
                "profile_id": current_user.profile_id
            }
        )
    return response

async def schedule_booking(request: ScheduleBookingRequest, booking_id: int): 
    async with database.connection(): 
        for time in request.times: 
            response = await database.execute(
                query="""
                    INSERT INTO timeslot (
                        booking_id, 
                        date_time
                    ) VALUES (
                        :booking_id, 
                        :date_time
                    )
                """, 
                values={
                    "booking_id": booking_id,
                    "date_time": time
                }
            )
            if response is None: 
                return False
    return True

async def booking_exists(booking_id: str): 
    async with database.connection(): 
        response = await database.fetch_one(
            query="SELECT * FROM booking WHERE booking_id=:booking_id",
            values={
                "booking_id": booking_id
            }
        )
    if response is None: 
        raise HTTPException("No booking found")
    return Booking(**dict(response))