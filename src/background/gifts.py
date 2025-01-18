import asyncio
from structlog.typing import FilteringBoundLogger
from aiogram import Bot 
from src.redis import RedisStorage



async def check_new_gifts(bot: Bot, redis: RedisStorage, logger: FilteringBoundLogger) -> bool:
    try:
        result = await bot.get_available_gifts()
        for item in result.gifts:
            item_id = int(item.id)
            if redis.add_gift(item_id):
                await logger.ainfo(f'new gift registered: {item_id}')
        return True
    except Exception as e:
        await logger.aerror(f"Error checking gifts: {e}")
        return False


async def background_gift_updator(
        bot: Bot, 
        redis: RedisStorage, 
        logger: FilteringBoundLogger, 
        vip_poll_interval: int,
        default_poll_interval: int
    ):
    while True:
        try:
            if await check_new_gifts(bot, redis, logger):
                await asyncio.sleep(vip_poll_interval)
                
                remaining_time = default_poll_interval - vip_poll_interval
                if remaining_time > 0:
                    await asyncio.sleep(remaining_time)
            else:
                await asyncio.sleep(default_poll_interval)
                
        except Exception as e:
            await logger.aerror(f"Error in background task: {e}")
            await asyncio.sleep(default_poll_interval)