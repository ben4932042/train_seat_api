import dataclasses
import datetime
from pydantic import BaseModel, validator
from typing import List


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
