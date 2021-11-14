from resources.seat_info import HighSpeedRailDomainKnowHow
from resources.seat_repo import HighSpeedRailSeatRepo


class SeatCalculator:
    def __init__(self):
        self.db_result = HighSpeedRailSeatRepo.get_all()

    def get_available_seat_number(self):
        return sum( [1 for seat in self.db_result if seat.available] )

    def get_business_available_seat_number(self):
        return sum( [1 for seat in self.db_result if seat.available and seat.is_business_car()] )

    def get_booking_seat(self):
        return [seat.only_car_and_seat_info() for seat in self.db_result if seat.booking]

    def get_available_seat_group_by_car(self):
        each_seat_info = {f"car_{i}": 0 for i in range( HighSpeedRailDomainKnowHow.car_number )}
        for seat in self.db_result:
            if seat.available: each_seat_info[f"car_{seat.car_no}"] += 1
        return each_seat_info