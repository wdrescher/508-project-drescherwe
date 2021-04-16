from typing import Optional

from pydantic import BaseModel
from api.models.requests import CreateParlorRequest

class Parlor(CreateParlorRequest): 
    parlor_id: str