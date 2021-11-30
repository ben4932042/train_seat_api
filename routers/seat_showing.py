from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, Query
from model.seat import *


router = APIRouter(
    prefix="/api/seat_showing",
    tags=["seat_showing"],
    responses={404: {"description": "Not found"}},
)



@router.get("/available_seat_no")
async def available_seat_no(request: Request):

        seat_dict = {}

        for i in range(10):
            raw_seat_dict = await request.app.state.redis.hgetall(i)
            seat_dict[f'car_{i}'] = [
                SeatInfo(*[int(key),int(raw_seat_dict[key])]).seat_no
                for key in raw_seat_dict.keys()
                if SeatInfo(*[int(key),int(raw_seat_dict[key])]).available()
            ]
            
        return HighSpeedRailSeatNo(**seat_dict)


@router.get("/available_seat_number")
async def available_seat_number(request: Request):

        seat_dict = {}
        
        for i in range(10):
            raw_seat_dict = await request.app.state.redis.hgetall(i)
            seat_dict[f'car_{i}'] = len([
                SeatInfo(*[int(key),int(raw_seat_dict[key])]).seat_no
                for key in raw_seat_dict.keys()
                if SeatInfo(*[int(key),int(raw_seat_dict[key])]).available()
            ])
            
        return HighSpeedRailSeatNumber(**seat_dict)

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
