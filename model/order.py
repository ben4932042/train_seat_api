import dataclasses
import datetime
from pydantic import BaseModel, validator
from typing import List


class OrderInfo(BaseModel):
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

@dataclasses.dataclass
class OrderWithTimeStampInfo:
    uuid: str
    car_no: int
    seat_no: int
    create_timestamp: float = dataclasses.field(init=False)
    delete_timestamp: float = dataclasses.field(init=False)
    def __post_init__(self):
        self.create_timestamp = datetime.datetime.now().timestamp()
        self.delete_timestamp = self.create_timestamp + (60*10)

@dataclasses.dataclass
class OrderToSeatInfo:
    ticket_info: str
    car_no: str = dataclasses.field(init=False)
    seat_no: int = dataclasses.field(init=False)
    delete_timestamp_str: str
    valid: bool = dataclasses.field(init=False)
    def __post_init__(self):
        car_seat_list = self.car_seat_info.split('_')

        if len(car_seat_list) != 2:
            raise ValueError("get unvalid car seat info.")

        self.car_no = f"car_{car_seat_list[0]}"
        self.seat_no = f"car_{car_seat_list[1]}" 
        self.valid = self.valid_order()

    def valid_order(self):
        return datetime.datetime.now().timestamp() <= float(self.delete_timestamp_str)    
