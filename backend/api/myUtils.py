import asyncio
import math
import os
from typing import Any, Coroutine

import redis.asyncio as redis
from aiohttp import ClientSession
from api.mySchemas import MyTimeoutError, scrapedProductSchema
from api.myScraper import getHTMLContent
from dotenv import load_dotenv
from redis.asyncio import StrictRedis

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

MAX_DURATION = 15


async def monitor(
    func: Coroutine[Any, Any, Any],
    redis_instance: StrictRedis | None = None,
    client: ClientSession | None = None,
):
    task = asyncio.create_task(func)
    try:
        async with asyncio.timeout(MAX_DURATION):
            return await task
    except TimeoutError:
        task.cancel()
        if isinstance(redis_instance, StrictRedis):
            await redis_instance.close()
        if isinstance(client, ClientSession):
            await client.close()
        raise MyTimeoutError("Time limit exceeded")


async def createRedisInstance():
    if REDIS_URL is not None:
        try:
            redis_instance = redis.StrictRedis.from_url(
                url=REDIS_URL, decode_responses=True, single_connection_client=True
            )
            ping = await redis_instance.ping()
            print(f"Redis Connection Established: {ping}")
            return redis_instance
        except:
            print("Error connecting to Redis server")
    return None


def splitIntoBatches(searchParams: list[str], paramsLength: int):
    partitions = 3
    batch_size = math.ceil(paramsLength / partitions)
    print(f"Batch Size: {batch_size}")
    batches: list[list[str]] = []
    for i in range(0, paramsLength, batch_size):
        batches.append(searchParams[i : i + batch_size])
    return batches


async def batchScrape(searchString: str, paramBatch: list[str], client: ClientSession):
    results: list[scrapedProductSchema] = []
    batchLength = len(paramBatch)

    redis_instance = await createRedisInstance()

    async def _batchScrape():
        scrape_tasks = [
            getHTMLContent(searchString, paramBatch[i], "", client, redis_instance)
            for i in range(batchLength)
        ]
        for results_future in asyncio.as_completed(scrape_tasks):
            result = await results_future
            if isinstance(result, list):
                results.extend(result)
        if isinstance(redis_instance, StrictRedis):
            await redis_instance.close()
        return results

    return await monitor(_batchScrape(), redis_instance, client)
