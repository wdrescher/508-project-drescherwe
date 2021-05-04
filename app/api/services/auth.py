from db import database
from uuid import uuid4
from passlib.context import CryptContext

from api.services.dependencies import get_user_from_email
from api.models.requests import SignupRequest, CreateClientRequest
from api.models.user import PrivateProfile, Profile

salt = "jibberish_that_you_would_never_ever_guess"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password): 
    return password_context.verify(salt + plain_password, hashed_password)

def hash_password(plain_password):
    return password_context.hash(salt + plain_password)

@database.transaction()
async def create_user(request: SignupRequest): 
    bearer_token: str = uuid4().__str__()
    hashed_password = hash_password(request.password)
    async with database.connection(): 
        result = await database.execute(
            query="""
                CALL create_user(:token, :email, :password, :first_name, :last_name)
            """, 
            values={
                "token": bearer_token, 
                "email": request.email, 
                "password": hashed_password, 
                "first_name": request.first_name, 
                "last_name": request.last_name
            }
        )
    if result is None: 
        raise "User already exists"

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

async def create_client(current_user: Profile, request: CreateClientRequest): 
    async with database.connection(): 
        result = await database.execute(
            query="""
                INSERT INTO client (
                    payment_id, 
                    contact_method, 
                    profile_id
                ) VALUES (
                    :payment_id, 
                    :contact_method, 
                    :profile_id
                )
            """, 
            values={
                "profile_id": current_user.profile_id, 
                "payment_id": request.payment_id, 
                "contact_method": request.contact_method
            }
        )
    assert result is not None
    return result

async def check_password(username: str, password: str): 
    profile = await get_user_from_email(username)
    if profile is None or not verify_password(password, profile.password): 
        return None
    return profile