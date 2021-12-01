import pickle
from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, status

from model.seat import *
from model.order import *
from model.ticket import *



router = APIRouter(
    prefix="/api/queue",
    tags=["queue"],
    responses={404: {"description": "Not found"}},
)

@router.post("/order_queue")
async def send_order_queue(request: Request, queue: TicketOrderQueue):
    await request.app.state.redis_queue.lpush('order_queue', pickle.dumps(queue.dict()))

@router.get("/order_queue")
async def get_order_queue(request: Request):
    data = await request.app.state.redis_queue.rpop('order_queue')
    if data:
        return pickle.loads(data)
    else:
        raise HTTPException(status_code=404, detail="No order in queue")

@router.post("/payment_queue")
async def send_order_queue(request: Request, uuid: str):
    await request.app.state.redis_queue.lpush('payment_queue', uuid)

@router.get("/payment_queue")
async def get_order_queue(request: Request):
    data = await request.app.state.redis_queue.rpop('payment_queue')
    if data:
        return {'uuid': data}
    else:
        raise HTTPException(status_code=404, detail="No payment in queue")

