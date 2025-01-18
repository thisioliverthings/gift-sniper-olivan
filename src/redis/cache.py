import json

from typing import List
from redis import Redis


class RedisStorage:
    def __init__(self, host: str, port: int) -> None:
        self.redis = Redis(
            host=host, port=port, decode_responses=True
        )
        self.vip_gifts_key = "vip_gifts_list"
        self.default_gifts_key = "default_gifts_list"

    def get_gifts(self, vip: bool = False) -> List[int]:
        if vip:
            # FOR VIP ONLY
            gifts = self.redis.get(self.vip_gifts_key)
            return json.loads(gifts) if gifts else []
        else:
            # FOR DEFAULT ONLY
            gifts = self.redis.get(self.default_gifts_key)
            return json.loads(gifts) if gifts else []

    def add_gift(self, gift_id: int, vip: bool = False) -> bool:
        if vip:
            # VIP = RICH, ONLY VIP CREATED 
            vip_gifts = self.get_gifts(vip=True)
            if gift_id not in vip_gifts:
                vip_gifts.append(gift_id)
                return self.redis.set(self.vip_gifts_key, json.dumps(vip_gifts))
        else:
            # NOT VIP = SHAWTY, VIP AND DEFAULT CREATED
            added = False
            
            vip_gifts = self.get_gifts(vip=True)
            if gift_id not in vip_gifts:
                vip_gifts.append(gift_id)
                self.redis.set(self.vip_gifts_key, json.dumps(vip_gifts))
                added = True
            
            default_gifts = self.get_gifts(vip=False)
            if gift_id not in default_gifts:
                default_gifts.append(gift_id)
                self.redis.set(self.default_gifts_key, json.dumps(default_gifts))
                added = True
            
            return added
        return False

    def clear_gifts(self) -> bool:
        return all([
            self.redis.delete(self.vip_gifts_key),
            self.redis.delete(self.default_gifts_key)
        ]) 