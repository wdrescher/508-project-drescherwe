from db import database

from uuid import uuid4
from api.models.requests import SignupRequest

@database.transaction()
async def create_user(request: SignupRequest): 
    bearer_token: str = uuid4().__str__()
    async with database.connection(): 
        result = await database.execute(
            query="""
                CALL create_user(:token, :email, :password, :first_name, :last_name)
            """, 
            values={
                "token": bearer_token, 
                "email": request.email, 
                "password": request.password, 
                "first_name": request.first_name, 
                "last_name": request.last_name
            }
        )
    if result is None: 
        raise "User not created"

    async with database.connection(): 
        token = await database.fetch_one(
            query="""
                SELECT * FROM token WHERE bearer=:token
            """, 
            values={
                "token":bearer_token
            }
        )
    if token is None: 
        raise "Token not found"
    return token