from aioredis import create_redis_pool, Redis
from fastapi import FastAPI


from routers import admin, seat_showing, seat_strategy, payment


app = FastAPI()

app.include_router(admin.router)
app.include_router(seat_showing.router)
app.include_router(seat_strategy.router)
app.include_router(payment.router)

async def get_redis_pool() -> Redis:
    redis = await create_redis_pool(f"redis://:@redis:6379/0?encoding=utf-8")
    return redis

@app.on_event("startup")
async def startup_event():
    app.state.redis = await get_redis_pool()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()
    await app.state.redis.wait_closed()

