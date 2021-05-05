from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer

from api.models.user import Profile, PrivateProfile, Artist
from db import database 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await get_user_from_token(token)
    return user

async def get_current_artist(current_user: Profile = Depends(get_current_user)):
    artist = await get_artist(current_user.profile_id)
    return artist

async def get_artist(profile_id: int): 
    async with database.connection(): 
        artist = await database.fetch_one(
            query="""
                SELECT * FROM artist WHERE profile_id=:profile_id
            """, 
            values={
                "profile_id": profile_id
            }
        )
    if artist is None: 
        return None
    return Artist(**dict(artist))

async def get_current_client(current_user: Profile = Depends(get_current_user)): 
    client =  await get_client(current_user)
    return client

async def get_client(current_user: Profile): 
    client = await database.fetch_one(
        query="""
            SELECT * FROM client WHERE profile_id=:profile_id
        """, 
        values={
            "profile_id": current_user.profile_id
        }
    )
    return client

async def get_user_from_id(profile_id: str): 
    async with database.connection(): 
        result = await database.fetch_one(
            query="SELECT * FROM profile WHERE profile_id=:profile_id", 
            values={'profile_id', profile_id}
        )
    if result is None: 
        raise "Profile not found"
    return Profile(**dict(result))

async def get_user_from_token(token: str): 
    async with database.connection(): 
        result = await database.fetch_one(
            query="""
                SELECT 
                    profile.profile_id, 
                    email, 
                    phone_number, 
                    first_name, 
                    last_name, 
                    artist.profile_id IS NOT NULL as is_artist
                FROM profile 
                LEFT JOIN artist 
                ON artist.profile_id = profile.profile_id
                WHERE token_id=:token
            """,
            values={'token': token}
        )
    if result is None: 
        raise HTTPException(status=400, detail="Token not validated")
    return Profile(**dict(result))

async def get_user_from_email(email: str):
    async with database.connection(): 
        profile = await database.fetch_one(
            query="""
                SELECT * FROM profile WHERE email=:email
            """, 
            values={"email": email}
        )
    if profile is not None:  
        return PrivateProfile(**dict(profile))
    else: 
        print(profile)
    return 