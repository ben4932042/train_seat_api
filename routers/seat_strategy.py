import datetime
from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, status
from typing import List

from model.seat import *
from model.order import *


router = APIRouter(
    prefix="/api/seat_strategy",
    tags=["seat_strategy"],
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

@router.post("/order", status_code=status.HTTP_201_CREATED)
async def order(request: Request, orders: List[OrderInfo], uuid: str):
        
        for seat_info in orders:
            car_no = seat_info.car_no
            seat_no = seat_info.seat_no
            now_status = await request.app.state.redis.hget(car_no, seat_no)
            if now_status != '1':
                raise HTTPException(status_code=403, detail="seat status vertify error")

        for seat_info in orders:
            order_info = OrderWithTimeStampInfo(
                uuid=uuid,
                car_no=seat_info.car_no,
                seat_no=seat_info.seat_no,
                )

            request.app.state.redis_order.hset(
                    order_info.uuid,
                    f"{order_info.car_no}_{order_info.seat_no}",
                    order_info.delete_timestamp
                    )

            request.app.state.redis.hset(order_info.car_no, order_info.seat_no, 2)
