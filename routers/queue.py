import pickle
from aioredis import create_redis_pool, Redis
from fastapi import APIRouter, HTTPException, Request, status

from model.seat import *
from model.order import *
from model.ticket import *
from model.default import *


router = APIRouter(
    prefix="/api/queue",
    tags=["queue"],
    responses={404: {"description": "Not found"}},
)

@router.post("/order_queue")
async def send_order_queue(request: Request, queue: TicketOrderQueue):
    await request.app.state.redis_queue.lpush('order_queue', pickle.dumps(queue.dict()))
    return DefaultSuccessReturn()

@router.get("/order_queue")
async def get_order_queue(request: Request):
    data = await request.app.state.redis_queue.rpop('order_queue')
    if not data:
        raise HTTPException(status_code=404, detail="No order in queue")

    return pickle.loads(data)
@router.post("/payment_queue")
async def send_order_queue(request: Request, uuid: str):
    await request.app.state.redis_queue.lpush('payment_queue', uuid)
    return DefaultSuccessReturn()

@router.get("/payment_queue")
async def get_order_queue(request: Request):
    data = await request.app.state.redis_queue.rpop('payment_queue')
    if not data:
        raise HTTPException(status_code=404, detail="No payment in queue")
    return {'uuid': data}
