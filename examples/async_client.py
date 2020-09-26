import asyncio
import httpx
import time

import zeep

from zeep.transports import AsyncTransport


def run_async():
    print("async example")
    print("=============")

    result = []

    def handle_future(future):
        result.extend(future.result())

    loop = asyncio.get_event_loop()

    client = zeep.AsyncClient("http://localhost:8000/?wsdl")

    tasks = [
        client.service.slow_request("request-1"),  # takes 1 sec
        client.service.slow_request("request-2"),  # takes 1 sec
    ]
    future = asyncio.gather(*tasks, return_exceptions=True)

    result = []
    future.add_done_callback(handle_future)

    st = time.time()
    loop.run_until_complete(future)
    loop.run_until_complete(client.transport.aclose())
    print("time: %.2f" % (time.time() - st))
    print("result: %s", result)
    print("")
    return future


def run_sync():
    print("sync example")
    print("============")
    transport = zeep.Transport(cache=None)
    client = zeep.Client("http://localhost:8000/?wsdl", transport=transport)

    st = time.time()
    result = [
        client.service.slow_request("request-1"),  # takes 1 sec
        client.service.slow_request("request-2"),  # takes 1 sec
    ]
    print("Time: %.2f" % (time.time() - st))
    print("result: %s", result)
    print("\n")

    return result


if __name__ == "__main__":
    print("")
    #asyncio.run(run_async())
    run_async()
    run_sync()
