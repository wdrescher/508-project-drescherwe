from pydantic import BaseModel

class TokenResponse(BaseModel): 
    bearer: str
    expiration_date: str