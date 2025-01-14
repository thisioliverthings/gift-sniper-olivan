import asyncio
from structlog.typing import FilteringBoundLogger

from aiogram import Bot 

from src.redis import RedisStorage


async def background_gift_updator(
        bot: Bot, 
        redis: RedisStorage, 
        logger: FilteringBoundLogger, 
        vip_poll_interval: int,
        default_poll_interval: int
    ):
    while True:
        try:
            result = await bot.get_available_gifts()
        except:
            await asyncio.sleep(10)
            continue

        for item in result.gifts:
            item_id = int(item.id)
            if redis.add_gift(item_id):
                await logger.ainfo(f'new gift registered: {item_id}')

        await asyncio.sleep(vip_poll_interval)