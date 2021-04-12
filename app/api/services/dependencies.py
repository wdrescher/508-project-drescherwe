from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from api.models.user import Profile
from db import database 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user_from_token(token)
    return user


async def get_user(profile_id: str): 
    async with database.connection(): 
        result = await database.fetch_one(
            query="SELECT * FROM profile WHERE profile_id=:profile_id", 
            values={'profile_id', profile_id}
        )
    if result is None: 
        raise "User not found"
    return Profile(result)

async def get_user_from_token(token: str): 
    async with database.connection(): 
        result = database.fetch_one(
            query="SELECT * FROM profile WHERE token_id=:token",
            values={'token': token}
        )
    if result is None: 
        raise "Token not found"
    return Profile(result)