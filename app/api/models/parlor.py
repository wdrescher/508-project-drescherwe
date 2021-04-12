from typing import Optional

from pydantic import BaseModel

class Parlor(BaseModel): 
    parlor_id: str
    name: str
    address_line_1: str
    address_line_2: [Optional]str = None
    city: str
    state: str
    zip: int
    shop_commission: int
    