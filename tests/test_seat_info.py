import pytest

from resources.seat_info import HighSpeedRailSeatInfo
from resources.seat_calculator import SeatCalculator


# @pytest.fixture()
# def fake_status(status):


def test_invalid_seat_status():
    with pytest.raises( ValueError ):
        HighSpeedRailSeatInfo( car_no=10, seat_no=0, status='paid' )
    with pytest.raises( ValueError ):
        HighSpeedRailSeatInfo( car_no=0, seat_no=50, status='paid' )
    with pytest.raises( ValueError ):
        HighSpeedRailSeatInfo( car_no=0, seat_no=0, status='' )


def test_get_available_seat_number_with_one_ticket(mocker):
    mocker.patch(
        'resources.seat_repo.HighSpeedRailSeatRepo.get_all',
        return_value=[
            HighSpeedRailSeatInfo( car_no=0, seat_no=0, status='available' ),
        ]
    )

    assert SeatCalculator().get_available_seat_number() == 1


def test_get_available_seat_number_with_multi_ticket(mocker):
    mocker.patch(
        'resources.seat_repo.HighSpeedRailSeatRepo.get_all',
        return_value=[
            HighSpeedRailSeatInfo( car_no=0, seat_no=0, status='available' ),
            HighSpeedRailSeatInfo( car_no=0, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=0, seat_no=2, status='paid' ),
        ]
    )
    assert SeatCalculator().get_available_seat_number() == 2


def test_get_available_seat_number_in_business_car(mocker):
    mocker.patch(
        'resources.seat_repo.HighSpeedRailSeatRepo.get_all',
        return_value=[
            HighSpeedRailSeatInfo( car_no=0, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=1, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=2, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=3, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=4, seat_no=1, status='available' ),
        ]
    )
    assert SeatCalculator().get_business_available_seat_number() == 3


def test_show_booking_seat(mocker):
    mocker.patch(
        'resources.seat_repo.HighSpeedRailSeatRepo.get_all',
        return_value=[
            HighSpeedRailSeatInfo( car_no=0, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=1, seat_no=1, status='booking' ),
            HighSpeedRailSeatInfo( car_no=2, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=3, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=4, seat_no=1, status='paid' ),
        ]
    )

    assert SeatCalculator().get_booking_seat() == [{'car_no': 1, 'seat_no': 1}]


def test_get_all_available_seat_group_by_car(mocker):
    mocker.patch(
        'resources.seat_repo.HighSpeedRailSeatRepo.get_all',
        return_value=[
            HighSpeedRailSeatInfo( car_no=0, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=1, seat_no=1, status='booking' ),
            HighSpeedRailSeatInfo( car_no=2, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=2, seat_no=1, status='available' ),
            HighSpeedRailSeatInfo( car_no=3, seat_no=1, status='paid' ),
        ]
    )

    assert SeatCalculator().get_available_seat_group_by_car() == {
        'car_0': 1,
        'car_1': 0,
        'car_2': 2,
        'car_3': 0,
        'car_4': 0,
        'car_5': 0,
        'car_6': 0,
        'car_7': 0,
        'car_8': 0,
        'car_9': 0
    }
