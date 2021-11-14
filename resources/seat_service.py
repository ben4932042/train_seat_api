from flask_restful import Resource

from resources.seat_calculator import SeatCalculator


class SeatInfoService( Resource ):
    def get(self, info_type):
        seat = SeatCalculator()
        if info_type == 'available_seat_no':
            return seat.get_available_seat_number()
        elif info_type == 'business_seat_no':
            return seat.get_business_available_seat_number()
        elif info_type == 'booking_list':
            return seat.get_booking_seat()
        elif info_type == 'all_available_seat':
            return seat.get_available_seat_group_by_car()
