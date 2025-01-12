import json

from typing import List
from redis import Redis


class RedisStorage:
    def __init__(self, host: str, port: int) -> None:
        self.redis = Redis(
            host=host, port=port, decode_responses=True
        )
        self.gifts_key = "gifts_list"

    def get_gifts(self) -> List[int]:
        gifts = self.redis.get(self.gifts_key)
        return json.loads(gifts) if gifts else []

    def add_gift(self, gift_id: int) -> bool:
        gifts = self.get_gifts()
        if gift_id not in gifts:
            gifts.append(gift_id)
            return self.redis.set(self.gifts_key, json.dumps(gifts))
        return False

    def clear_gifts(self) -> bool:
        return self.redis.delete(self.gifts_key) 