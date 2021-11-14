from typing import List

from resources.seat_info import HighSpeedRailSeatInfo


class HighSpeedRailSeatRepo:
    @staticmethod
    def get_all() -> List[HighSpeedRailSeatInfo]:
        # TODO
        # Redis Connection

        return [
            HighSpeedRailSeatInfo( car_no=0, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=1, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=2, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=3, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=4, seat_no=1, status='booking' ),
        ]
