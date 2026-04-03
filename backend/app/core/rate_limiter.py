import time
from collections import defaultdict
from typing import Tuple

class RateLimiter:
    def __init__(self, rate: int = 100, per_seconds: int = 60):
        self.rate = rate
        self.per_seconds = per_seconds
        self.tokens = defaultdict(float)
        self.last_refill = defaultdict(float)
    
    async def is_allowed(self, key: str) -> Tuple[bool, int]:
        now = time.time()
        time_passed = now - self.last_refill[key]
        new_tokens = time_passed * (self.rate / self.per_seconds)
        self.tokens[key] = min(self.rate, self.tokens[key] + new_tokens)
        self.last_refill[key] = now
        
        if self.tokens[key] >= 1:
            self.tokens[key] -= 1
            return True, 0
        else:
            wait_time = (1 - self.tokens[key]) * (self.per_seconds / self.rate)
            return False, int(wait_time) + 1
