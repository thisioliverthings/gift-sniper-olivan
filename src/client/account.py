from pyrogram import Client

from src.config import Config
from src.utils import CRYPTO_BOT_USERNAME


async def get_session(config: Config):
    client = Client(
        "src/client/session/default",
        api_id=config.api_id,
        api_hash=config.api_hash,
        phone_number=config.phone_number,
        system_version="4.16.30-vxCUSTOM"
    )
    await client.start()
    return client


async def send_gift(client: Client, user_id: int, gift_id: int):
    try:
        await client.send_gift(user_id, gift_id)
        return True
    except:
        return False
    

async def cryptobot_invoice_register(client: Client, user_id: int, checkout: str) -> int:
    await client.send_message(
        CRYPTO_BOT_USERNAME, 'test'
    )