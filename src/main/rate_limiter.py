import asyncio
import os
import time
from typing import Any
from typing import Callable
from typing import Coroutine
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from telegram._utils.types import JSONDict
from telegram.ext._baseratelimiter import BaseRateLimiter
from telegram.ext._utils.types import RLARGS

from logger import Logger

this_dir = os.path.dirname(__file__)
logger_rel_path = '../../spinnit.log'
logger_abs_path = os.path.join(this_dir, logger_rel_path)
rate_limiter_logger = Logger('rate_limiter', logger_abs_path)


class RateLimiter(BaseRateLimiter):
    def __init__(self):
        self.private_chat_timestamps = []
        self.group_timestamps = {}

    async def initialize(self) -> None:
        pass

    async def shutdown(self) -> None:
        pass

    async def process_request(
            self,
            callback: Callable[..., Coroutine[Any, Any, Union[bool, JSONDict, List[JSONDict]]]],
            args: Any,
            kwargs: Dict[str, Any],
            endpoint: str,
            data: Dict[str, Any],
            rate_limit_args: Optional[RLARGS],
    ) -> Union[bool, JSONDict, List[JSONDict]]:
        chat_id = data.get('chat_id')
        if chat_id:
            if chat_id > 0:
                # private chat
                now = time.time()
                self.private_chat_timestamps = [ts for ts in self.private_chat_timestamps if ts + 1 > now - 1]
                if len(self.private_chat_timestamps) >= 30:
                    time_to_wait = self.private_chat_timestamps[0] + 1 - now
                    rate_limiter_logger.log('warning', f"Global private chat rate limit (30 msg/s) hit! Sleeping for"
                                                       f" {time_to_wait} seconds")
                    await asyncio.sleep(time_to_wait)
                self.private_chat_timestamps.append(now)
            else:
                # group/supergroup/channel chat
                now = time.time()
                chat_timestamps = self.group_timestamps.get(chat_id, [])
                chat_timestamps = [ts for ts in chat_timestamps if ts + 60 > now - 1]
                if len(chat_timestamps) >= 20:
                    time_to_wait = chat_timestamps[0] + 60 - now
                    rate_limiter_logger.log('warning', f"Group/supergroup/channel chat rate limit (20 msg/min) hit! "
                                                       f"Sleeping for {time_to_wait} seconds")
                    await asyncio.sleep(time_to_wait)
                chat_timestamps.append(now)
                self.group_timestamps[chat_id] = chat_timestamps
        return await callback(*args, **kwargs)
