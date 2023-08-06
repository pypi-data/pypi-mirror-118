import asyncio
# import nest_asyncio
import traceback
import time
import sys


__ALL__ = ["ThreadWrapper_async"]


class ThreadWrapper_async:
    def __init__(self, semaphore: asyncio.Semaphore, loop: asyncio.AbstractEventLoop) -> None:
        self.total_thread_count = 0
        self.sema = semaphore
        self.tasks = []
        self.loop = loop
        # nest_asyncio.apply(self.loop)
        self.debug_time = False

    async def __run_job(self, job: asyncio.coroutine, result, key):
        try:
            await self.sema.acquire()
            start_time = time.time()
            if isinstance(result, list):
                result.append(await job)
            elif isinstance(result, dict):
                result[key] = await job
            duration = time.time()-start_time
            if self.debug_time:
                count = str(self.total_thread_count).ljust(20)
                qualname = job.__qualname__.ljust(50)
                timestamp = str(int(time.time() * 1000) / 1000).ljust(20)[6:]
                s = f"Thread {count}{qualname}{timestamp}{duration}s\n"
                if duration >= 0.5:
                    sys.stderr.write(s)
                    sys.stderr.flush()
                else:
                    print(s, flush=True)
        except:
            traceback.print_exc()
        finally:
            self.sema.release()

    def add(self, job: asyncio.coroutine, result = None, key = None):
        if result is None:
            result = {}
        if key is None:
            key = 0
        job = asyncio.ensure_future(job, loop=self.loop)
        job = self.__run_job(job, result, key)
        self.tasks.append(job)
        return True

    def wait(self, run_type=None):
        asyncio.set_event_loop(self.loop)

        async def main():
            return await asyncio.gather(*self.tasks, loop=self.loop)

        if run_type == "run_forever":
            return self.loop.run_forever()
        else:
            return self.loop.run_until_complete(main())
