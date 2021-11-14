from resources.seat_info import HighSpeedRailSeatInfo

def test_available_seat_no(mocker, client):
    mocker.patch(
        'resources.seat_repo.HighSpeedRailSeatRepo.get_all',
        return_value=[
            HighSpeedRailSeatInfo( car_no=0, seat_no=0, status='available' ),
        ]
    )

    rv = client.get('/api/seat/available_seat_no')
    assert rv.status_code == 200
    assert 1 in rv.data