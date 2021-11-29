from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, status
from model.seat import *


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

@router.post("/seat_status", status_code=status.HTTP_201_CREATED)
async def seat_status(request: Request, car_no: int, seat_no: int):

        now_status = await request.app.state.redis.hget(car_no, seat_no)

        if now_status == '1':
            request.app.state.redis.hset(car_no, seat_no, 2)
        else:
            raise HTTPException(status_code=403, detail="seat status vertify error")
