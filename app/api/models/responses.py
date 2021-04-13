from pydantic import BaseModel
from datetime import date

class TokenResponse(BaseModel): 
    bearer: str
    expiration_date: date