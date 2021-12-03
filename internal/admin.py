from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, Query


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.delete("/reset_seat_status")
async def reset_seat_status(request: Request, car_no: int=Query(default=None)):
        """[summary] \n
        0 means seat is paid. \n
        1 means seat is available. \n
        2 means seat is locked. \n
        """
        
        if car_no is not None:
            car_list = [car_no]
        else:
            car_list = [i for i in range(10)]
        for i in car_list:
            for j in range(50):
                await request.app.state.redis.hset(i,j,1)
        

        return {'message': 'success'}

@router.delete("/reset_order")
async def reset_order(request: Request):
        await request.app.state.redis_order.flushdb()
        return {'message': 'success'}

@router.get("/all_order")
async def all_order(request: Request):
        order_list = await request.app.state.redis_order.keys(pattern='*')
        return {'orders': order_list}

