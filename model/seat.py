import dataclasses
from pydantic import BaseModel
from typing import List


@dataclasses.dataclass
class SeatInfo:
    seat_no: int
    status: int

    def __post_init__(self):

        if self.seat_no not in range(50):
            raise ValueError( 'get invalid seat number' )
        if self.status not in range(3):
            raise ValueError('get invalid seat status')

    def available(self):
        return self.status == 1
    def booking(self):
        return self.status == 2
    def paid(self):
        return self.status == 0

class HighSpeedRailFullSeatInfo(BaseModel):
    car_0: List[SeatInfo]
    car_1: List[SeatInfo]
    car_2: List[SeatInfo]
    car_3: List[SeatInfo]
    car_4: List[SeatInfo]
    car_5: List[SeatInfo]
    car_6: List[SeatInfo]
    car_7: List[SeatInfo]
    car_8: List[SeatInfo]
    car_9: List[SeatInfo]

class HighSpeedRailSeatNo(BaseModel):
    car_0: List[int]
    car_1: List[int]
    car_2: List[int]
    car_3: List[int]
    car_4: List[int]
    car_5: List[int]
    car_6: List[int]
    car_7: List[int]
    car_8: List[int]
    car_9: List[int]

class HighSpeedRailSeatNumber(BaseModel):
    car_0: int
    car_1: int
    car_2: int
    car_3: int
    car_4: int
    car_5: int
    car_6: int
    car_7: int
    car_8: int
    car_9: int


