import time
from aioredis import create_redis_pool, Redis
from fastapi import FastAPI, Request
from fastapi_contrib.tracing.middlewares import OpentracingMiddleware
from fastapi_contrib.tracing.utils import setup_opentracing


from routers import seat_showing, seat_strategy, payment, queue
from internal import admin
import config

description = """
Seat API 幫助所有需要得到座位相關訊息的開發者獲得他們想要的資訊. 🚀

## admin
WARNING: 任何用戶服務不得串接此路線下的所有接口

此路線用於 admin 相關系統重置與系統調教之使用

* **[DELETE]** reset_seat_status: 重置座位訊息
* **[DELETE]** reset_order: 重置訂單訊息
* **[GET]** all_order: 獲得所有訂單編號

## seat_showing

* **[GET]** available_seat_no: 獲得詳細可訂位座位訊息
* **[GET]** available_seat_number: 獲得可訂位座位數量
* **[GET]** order: 查詢單筆訂單資訊

## seat_strategy

* **[GET]** available_seat_no: 獲得詳細可訂位座位訊息
* **[GET]** available_seat_number: 獲得可訂位座位數量
* **[POST]** order: 新增一筆訂單

## payment

* **[GET]** booking_seat_no: 獲得詳細已訂位座位訊息
* **[PATCH]** seat_status: 修改座位狀態為已付款
* **[GET]** order: 查詢單筆訂單資訊


"""
tags_metadata = [
    {
        "name": "admin",
        "description": "",
    },
    {
        "name": "queue",
        "description": "",
    },
    {
        "name": "seat_showing",
        "description": "",
    },
    {
        "name": "seat_strategy",
        "description": "",
    },
    {
        "name": "payment",
        "description": "",
    },

]



app = FastAPI(
    title="Seat API",
    description=description,
    openapi_tags=tags_metadata,
    version="1.0.0-release",
    docs_url="/api/docs",
    redoc_url=None
    )

app.include_router(admin.router)
app.include_router(queue.router)
app.include_router(seat_showing.router)
app.include_router(seat_strategy.router)
app.include_router(payment.router)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

async def get_seat_pool() -> Redis:
    redis_config = config.RedisSettings() 
    redis = await create_redis_pool(f"redis://:@{redis_config.host}:{redis_config.port}/0?encoding=utf-8")
    return redis

async def get_order_pool() -> Redis:
    redis_config = config.RedisSettings() 
    redis_order = await create_redis_pool(f"redis://:@{redis_config.host}:{redis_config.port}/1?encoding=utf-8")
    return redis_order

async def get_queue_pool() -> Redis:
    redis_config = config.RedisSettings() 
    redis_order = await create_redis_pool(f"redis://:@{redis_config.host}:{redis_config.port}/2")
    return redis_order

@app.on_event('startup')
async def startup():
    setup_opentracing(app)
    app.add_middleware(OpentracingMiddleware)


@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_seat_pool()
    app.state.redis_order = await get_order_pool()
    app.state.redis_queue = await get_queue_pool()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    app.state.redis_order.close()
    app.state.redis_queue.close()
    await app.state.redis.wait_closed()
    await app.state.redis_order.wait_closed()
    await app.state.redis_queue.wait_closed()
