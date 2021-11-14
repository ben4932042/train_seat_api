import dataclasses


@dataclasses.dataclass
class HighSpeedRailDomainKnowHow:
    car_number: int = 10
    seat_number: int = 50


@dataclasses.dataclass
class HighSpeedRailSeatInfo:
    car_no: int
    seat_no: int
    status: str
    available: bool = False
    booking: bool = False
    paid: bool = False

    def __post_init__(self):
        if self.car_no not in range( HighSpeedRailDomainKnowHow.car_number ):
            raise ValueError( 'get invalid car number.' )
        elif self.seat_no not in range( HighSpeedRailDomainKnowHow.seat_number ):
            raise ValueError( 'get invalid seat number' )

        if self.status == 'available':
            self.available = True
        elif self.status == 'booking':
            self.booking = True
        elif self.status == 'paid':
            self.paid = True
        else:
            raise ValueError( 'get invalid seat status' )

    def is_business_car(self):
        return self.car_no in range( 3 )

    def only_car_and_seat_info(self):
        return {
            'car_no': self.car_no,
            'seat_no': self.seat_no
        }


