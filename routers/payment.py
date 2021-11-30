from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, status

from model.seat import *
from model.order import *
from model.ticket import *

router = APIRouter(
    prefix="/api/payment",
    tags=["payment"],
    responses={404: {"description": "Not found"}},
)

@router.get("/booking_seat_no")
async def booking_seat_no(request: Request) -> HighSpeedRailSeatNo:

        seat_dict = {}

        for i in range(10):
            raw_seat_dict = await request.app.state.redis.hgetall(i)
            seat_dict[f'car_{i}'] = [
                SeatInfo(*[int(key),int(raw_seat_dict[key])]).seat_no
                for key in raw_seat_dict.keys()
                if SeatInfo(*[int(key),int(raw_seat_dict[key])]).booking()
            ]
            
        return HighSpeedRailSeatNo(**seat_dict)


@router.post("/seat_status", status_code=status.HTTP_201_CREATED)
async def seat_status(request: Request, ticket: TicketInfo) -> None:
        now_status = await request.app.state.redis.hget(ticket.car_no, ticket.seat_no)

        if now_status == '2':
            request.app.state.redis.hset(ticket.car_no, ticket.seat_no, 0)
        else:
            raise HTTPException(status_code=403, detail="seat status vertify error")

@router.get("/order")
async def order(request: Request, uuid: str):

        info_dict = await request.app.state.redis_order.hgetall(uuid)
        return_list = []
        while True:
            try:
                return_list.append(
                        OrderToSeatInfo(**dict(zip(
                            ['ticket_info', 'delete_timestamp_str'],
                            info_dict.popitem()
                                ))
                            )
                        )
            except KeyError:
                break
        return return_list
