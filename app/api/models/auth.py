from pydantic import BaseModel

class Token(BaseModel): 
    bearer: str
    expiration_date: str