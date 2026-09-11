import time

class TokenBucket:
    def __init__(self, capacity:int, refill_rate:float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill_time = time.time()

    def _refill(self):
        time_now = time.time()
        time_passed = time_now - self.last_refill_time
        tokens_to_add = time_passed * self.refill_rate
        new_tokens = self.tokens + tokens_to_add
        self.tokens = min(self.capacity, new_tokens)
        self.last_refill_time = time_now

    def allow_request(self):
        self._refill()
        if self.tokens>=1:
            self.tokens-=1
            return True
        return False

class RateLimiter:

    def __init__(self, capacity:int, refill_rate:float):
        self.request_map = {}
        self.capacity = capacity
        self.refill_rate = refill_rate

    def check_request(self, userID:int):
        if userID not in self.request_map: 
            self.request_map[userID] = TokenBucket(self.capacity, self.refill_rate)
        request_status = self.request_map[userID].allow_request()
        return request_status




