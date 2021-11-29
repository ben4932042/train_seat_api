from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, Query


router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    responses={404: {"description": "Not found"}},
)

@router.post("/reset_seat_status")
async def reset_seat_status(request: Request, car_no: int=Query(default=None)):
        """[summary] \n
        0 means seat is paid. \n
        1 means seat is available. \n
        2 means seat is locked. \n
        """
        
        if car_no is None:
            for i in range(10):
                for j in range(50):
                    await request.app.state.redis.hset(i,j,1)
        

        return {'message': 'success'}

