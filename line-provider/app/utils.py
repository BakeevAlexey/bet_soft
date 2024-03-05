import redis.asyncio as redis


async def get_redis_connection() -> redis.Redis:
    """Подключение к redis."""
    return await redis.Redis(host='redis', port=6379, decode_responses=True)