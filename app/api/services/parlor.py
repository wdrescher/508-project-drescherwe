from fastapi import HTTPException
from db import database

from api.models.requests import CreateParlorRequest
from api.models.parlor import Parlor

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

async def create_parlor(request: CreateParlorRequest): 
    async with database.connection(): 
        result = await database.fetch_one(
            query="""
                SELECT create_parlor(
                    :address_line_1, 
                    :address_line_2,
                    :city, 
                    :name, 
                    :shop_commission,
                    :state,
                    :zip
                );
            """, 
            values={
                "address_line_1": request.address_line_1, 
                "address_line_2": request.address_line_2, 
                "city": request.city, 
                "name": request.name, 
                "shop_commission": request.shop_commission, 
                "state": request.state, 
                "zip": request.zip
            }
        )
        parlor_id = result[0]
        assert parlor_id is not None

        parlor = await database.fetch_one(
            query="""
                SELECT * FROM parlor WHERE parlor_id = :parlor_id
            """, 
            values={
                'parlor_id': parlor_id
            }
        )

    return Parlor(**dict(parlor))