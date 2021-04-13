from pydantic import BaseModel

class SignupRequest(BaseModel): 
    email: str
    password: str
    first_name: str
    last_name: str


class AccessRequest(BaseModel): 
    email: str
    password: str

class ResetPasswordRequest(BaseModel): 
    profile_id: str
    new_password: str