from typing import Any, Awaitable, Callable, Generic, List, TypeVar
import asyncio
import random
import logging
import traceback


logger = logging.getLogger(__name__)


class EntryProcessor:
    async def aprocess(self,
        entry: Any,
    ) -> List[Any]:
        pass


class PassthruProcessor(EntryProcessor):
    async def aprocess(self,
        entry: Any,
    ) -> List[Any]:
        return [entry]


I = TypeVar("I")
O = TypeVar("O")

class RetryWrapper(Generic[I, O]):
    async def aretry(self,
        entry: I,
        func_handler: Callable[[I], Awaitable[O]],
        max_retry_count: int = 5,
    ) -> O:
        iteration_count = 0
        is_value_set = False
        out: O = None
        while iteration_count < max_retry_count:
            iteration_count += 1
            try:
                out = await func_handler(entry)
                is_value_set = True
                break
            except Exception as e:
                sleep_time_s = 10 * (1.5) ** iteration_count + random.randrange(2,8)
                logger.error(
                    "[iteration:%d] Sleeping %f seconds after receiving message has failure: %s",
                    iteration_count,
                    sleep_time_s,
                    e,
                )
                traceback.print_exc()
                await asyncio.sleep(sleep_time_s)
                continue

        if not is_value_set:
            raise RuntimeError("failed even after %d retries." % max_retry_count)

        return out