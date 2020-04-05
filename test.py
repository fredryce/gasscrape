import time
import asyncio
from concurrent.futures import ProcessPoolExecutor

def blocking_func(x):
   time.sleep(x) # Pretend this is expensive calculations
   return x * 5

@asyncio.coroutine
def main():
    #pool = multiprocessing.Pool()
    #out = pool.apply(blocking_func, args=(10,)) # This blocks the event loop.
    executor = ProcessPoolExecutor()
    out = yield from loop.run_in_executor(executor, blocking_func, 10)  # This does not
    print(out)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())




import asyncio
import requests

async def main():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
    response1 = await future1
    response2 = await future2
    print(response1.text)
    print(response2.text)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())