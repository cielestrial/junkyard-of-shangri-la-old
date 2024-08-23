import asyncio
import math
import os
from typing import Any, Coroutine

import redis.asyncio as redis
from aiohttp import ClientSession
from .my_schemas import MyTimeoutError, ScrapedProductSchema
from .my_scraper import get_html_content
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
            await redis_instance.aclose()
        if isinstance(client, ClientSession):
            await client.close()
        raise MyTimeoutError("Time limit exceeded")


async def create_redis_instance():
    if REDIS_URL is not None:
        async with redis.StrictRedis.from_url(
            url=REDIS_URL, decode_responses=True, single_connection_client=True
        ) as redis_instance:
            try:
                ping = await redis_instance.ping()
                print(f"Redis Connection Established: {ping}")
                return redis_instance
            except:
                print("Error connecting to Redis server")
    return None


def split_into_batches(search_params: list[str], param_length: int):
    partitions = 3
    batch_size = math.ceil(param_length / partitions)
    print(f"Batch Size: {batch_size}")
    batches: list[list[str]] = []
    for i in range(0, param_length, batch_size):
        batches.append(search_params[i : i + batch_size])
    return batches


async def batch_scrape(
    search_string: str, param_batch: list[str], client: ClientSession
):
    results: list[ScrapedProductSchema] = []
    batch_length = len(param_batch)

    redis_instance = await create_redis_instance()

    async def _batch_scrape():
        scrape_tasks = [
            get_html_content(search_string, param_batch[i], "", client, redis_instance)
            for i in range(batch_length)
        ]
        for results_future in asyncio.as_completed(scrape_tasks):
            result = await results_future
            if isinstance(result, list):
                results.extend(result)
        if isinstance(redis_instance, StrictRedis):
            await redis_instance.aclose()
        return results

    return await monitor(_batch_scrape(), redis_instance, client)
