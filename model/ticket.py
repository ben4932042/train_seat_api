from pydantic import BaseModel, validator
from typing import List, Optional


class TicketInfo(BaseModel):
    car_no: int
    seat_no: int

    @validator('car_no')
    def car_rule(cls, v):
        if v not in range(10):
            raise ValueError("get invalid car number")
        return v

    @validator('seat_no')
    def seat_rule(cls, v):
        if v not in range(50):
            raise ValueError("get invalid seat number")
        return v

class TicketOrderQueue(BaseModel):
    uuid: str
    autoticket: bool
    prefer: Optional[int] = 0
    car_type: Optional[int] = None
    number: Optional[int] = None
    chosen_seats_list: List[TicketInfo] = None

    @validator('prefer')
    def prefer_rule(cls, v):
        if not v:
             return v
        if v not in range(2):
            raise ValueError("get invalid prefer type")
        return v

    @validator('car_type')
    def car_rule(cls, v):
        if not v:
             return v
        if v not in range(2):
            raise ValueError("get invalid car type")
        return v

    @validator('number')
    def number_rule(cls, v):
        if not v:
             return v
        if v not in [1, 2, 3, 4]:
            raise ValueError("get invalid number type")
        return v
