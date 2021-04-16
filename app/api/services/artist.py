from fastapi import HTTPException
from db import database

from api.models.user import Profile, Artist
from api.models.parlor import Parlor

async def create_artist(current_user: Profile, artist: Artist): 
    async with database.connection(): 
        response = await database.execute(
            query="""
                INSERT INTO artist (
                    is_manager, 
                    max_bookings, 
                    minimum_price, 
                    profile_id
                ) VALUES (
                    :is_manager, 
                    :max_bookings, 
                    :minimum_price, 
                    :profile_id
                )
            """, 
            values={
                "profile_id": current_user.profile_id, 
                "is_manager": artist.is_manager, 
                "max_bookings": artist.max_bookings, 
                "minimum_price": artist.minimum_price
            }
        )
    assert response is not None
    return response

async def edit_artist(current_user: Profile, artist: Artist):
    async with database.connection(): 
        result = await database.execute(
             query="""
                UPDATE artist SET 
                    is_manager=:is_manager, 
                    max_bookings=:max_bookings, 
                    minimum_price=:minimum_price, 
                    parlor_id=:parlor_id
                WHERE profile_id=:profile_id
            """, 
            values={
                "profile_id": current_user.profile_id, 
                "is_manager": artist.is_manager, 
                "max_bookings": artist.max_bookings, 
                "minimum_price": artist.minimum_price, 
                "parlor_id": artist.parlor_id
            }
        )
    assert result is not None
    return result

async def get_parlor(parlor_id: str): 
    async with database.connection(): 
        parlor = await database.fetch_one(
            query="""
            SELECT * FROM parlor WHERE parlor_id=:parlor_id
            """,
            values={
                "parlor_id": parlor_id
            }
        )
    if parlor is None: 
        raise HTTPException(status_code=404, detail="No parlor found")
    return Parlor(**dict(parlor))