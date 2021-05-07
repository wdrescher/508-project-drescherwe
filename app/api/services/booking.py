from datetime import datetime
from typing import List
from fastapi import HTTPException
from db import database

from api.models.requests import CreateBookingRequest, ScheduleBookingRequest
from api.models.user import Profile, Client
from api.models.booking import Booking

async def get_artist_bookings(current_user: Profile): 
    async with database.connection(): 
        response = await database.fetch_all(
            query="""
                SELECT 
                    artist_id, 
                    booking.booking_id, 
                    client_id, 
                    design_description, 
                    design_approved, 
                    price, 
                    price_approved, 
                    CONCAT(profile.first_name, " ", profile.last_name) as artist_name,
                    (
                        SELECT date_time 
                        FROM timeslot
                        WHERE timeslot.booking_id = booking.booking_id AND timeslot.selected = True
                        LIMIT 1
                    ) as selected_date
                FROM booking 
                JOIN profile 
                ON booking.client_id = profile.profile_id
                WHERE artist_id=:profile_id
            """, 
            values={
                "profile_id": current_user.profile_id
            }
        )
    return response

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
                SELECT 
                    artist_id, 
                    booking.booking_id, 
                    client_id, 
                    design_description, 
                    design_approved, 
                    price, 
                    price_approved, 
                    CONCAT(profile.first_name, " ", profile.last_name) as artist_name, 
                    (
                        SELECT date_time 
                        FROM timeslot
                        WHERE timeslot.booking_id = booking.booking_id AND timeslot.selected = True
                        LIMIT 1
                    ) as selected_date
                FROM booking 
                JOIN profile 
                ON booking.artist_id = profile.profile_id
                WHERE client_id=:profile_id
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
                UPDATE booking SET price=:price, price_approved=False, design_approved=True WHERE booking_id=:booking_id AND artist_id=:profile_id
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
                "approved": True, 
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
        raise HTTPException(status_code=400, detail='Booking does not exist')
    return Booking(**dict(response))

async def select_time(date_time: str, booking_id: int):
    async with database.connection(): 
        result = await database.execute(
            query="""
                UPDATE timeslot SET selected = (date_time = :date_time) WHERE booking_id = :booking_id 
            """, 
            values={
                "date_time": date_time, 
                "booking_id": booking_id
            }
        )
    return result

async def get_times(booking_id: int) -> List[datetime]:
    async with database.connection(): 
        result = await database.fetch_all(
            query="""
                SELECT date_time FROM timeslot WHERE booking_id = :booking_id; 
            """, 
            values={
                "booking_id": booking_id
            }
        ) 
    if result is None: 
        raise HTTPException(status_code=404, detail="bookings not found")
    list_response: List[datetime] = []
    for date in result: 
        list_response.append(date[0])
    return list_response