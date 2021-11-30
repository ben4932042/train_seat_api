from aioredis import create_redis_pool, Redis
from fastapi import FastAPI


from routers import admin, seat_showing, seat_strategy, payment
import config


app = FastAPI()

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
