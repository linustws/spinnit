import asyncio
import time
from telegram.ext import BaseRateLimiter


class RateLimiter(BaseRateLimiter):
    def __init__(self, rate_limit=1, rate_limit_period=30):
        self.rate_limit = rate_limit
        self.rate_limit_period = rate_limit_period
        self.request_history = {"sendAnimation": []}

    async def initialize(self):
        # Initialize any resources required by the rate limiter here
        pass

    async def process_request(
            self, callback, args, kwargs, endpoint, data, rate_limit_args
    ):
        if endpoint == "sendAnimation":
            now = time.time()
            self.request_history[endpoint] = [
                req for req in self.request_history[endpoint]
                if req >= now - self.rate_limit_period
            ]

            if len(self.request_history.get(endpoint, [])) >= self.rate_limit:
                sleep_time = (
                        self.request_history[endpoint][0]
                        + self.rate_limit_period
                        - now
                )
                print(sleep_time)
                await asyncio.sleep(sleep_time)

            self.request_history.setdefault(endpoint, []).append(now)

        return await callback(*args, **kwargs)

    async def shutdown(self):
        # Clean up any resources used by the rate limiter here
        pass
