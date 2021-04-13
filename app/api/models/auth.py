from pydantic import BaseModel
from datetime import date

class Token(BaseModel): 
    bearer: str
    expiration_date: date