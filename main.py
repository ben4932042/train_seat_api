from aioredis import create_redis_pool, Redis
from fastapi import FastAPI


from routers import seat_showing, seat_strategy, payment
from internal import admin
import config

description = """
Seat API 幫助所有需要得到座位相關訊息的開發者獲得他們想要的資訊. 🚀

## admin
WARNING: 任何用戶服務不得串接此路線下的所有接口

此路線用於 admin 相關系統重置與系統調教之使用

* **[DELETE]** reset_seat_status: 重置座位訊息
* **[DELETE]** reset_order: 重置訂單訊息
* **[GET]** all_order: 獲得所有訂單邊號

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
* **[GET]** booking_seat_no: 獲得已訂位座位數量
* **[POST]** seat_status: 修改座位狀態為已付款
* **[GET]** order: 查詢單筆訂單資訊


"""
tags_metadata = [
    {
        "name": "admin",
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
app.include_router(seat_showing.router)
app.include_router(seat_strategy.router)
app.include_router(payment.router)


async def get_redis_pool() -> Redis:
    redis_config = config.RedisSettings() 
    redis = await create_redis_pool(f"redis://:@{redis_config.host}:{redis_config.port}/0?encoding=utf-8")
    return redis

async def get_redis_order_pool() -> Redis:
    redis_config = config.RedisSettings() 
    redis_order = await create_redis_pool(f"redis://:@{redis_config.host}:{redis_config.port}/1?encoding=utf-8")
    return redis_order

@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()
    app.state.redis_order = await get_redis_order_pool()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    app.state.redis_order.close()
    await app.state.redis.wait_closed()
    await app.state.redis_order.wait_closed()
