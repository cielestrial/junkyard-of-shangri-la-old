import math
import os

import redis.asyncio as redis
from dotenv import load_dotenv
from myScraper import *

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")


async def createRedisInstance(single: bool):
    if REDIS_URL is not None:
        try:
            redis_instance = redis.StrictRedis.from_url(
                url=REDIS_URL, decode_responses=True, single_connection_client=single
            )
            ping = await redis_instance.ping()
            print(f"Redis Connection Established: {ping}")
            return redis_instance
        except:
            raise RedisConnectionError("Error connecting to Redis server")
    return asyncio.sleep(0)


def splitIntoBatches(searchParams: list[str], paramsLength: int):
    batch_size = math.ceil(paramsLength / 3)
    print(f"Batch Size: {batch_size}")
    batches: list[list[str]] = []
    for i in range(0, paramsLength, batch_size):
        batches.append(searchParams[i : i + batch_size])
    return batches


async def batchScrape(searchString: str, paramBatch: list[str], client: ClientSession):
    results: list[scrapedProductSchema] = []
    batchLength = len(paramBatch)

    redis_instance = await createRedisInstance(False)
    if not isinstance(redis_instance, Redis):
        redis_instance = None
    scrape_tasks = [
        getHTMLContent(searchString, paramBatch[i], "", client, redis_instance)
        for i in range(batchLength)
    ]
    for results_future in asyncio.as_completed(scrape_tasks):
        result = await results_future
        if isinstance(result, list):
            results.extend(result)
    if isinstance(redis_instance, Redis):
        await redis_instance.close()
    return results
