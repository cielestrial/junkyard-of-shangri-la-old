import os

import redis.asyncio as redis
from aiohttp import ClientSession
from dotenv import load_dotenv
from redis.asyncio import Redis
from src.bookScraper import *
from src.errors import *

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")
REDIS_MAX_CLIENTS = os.getenv("REDIS_MAX_CLIENTS")


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


def getWebsiteUrl(paramURL: str):
    """Returns the url for the provided domain name."""
    url = {
        "baseURL": "https://books.toscrape.com/",
        "subURL": "catalogue/",
        "extendedURL": f"category/books/{paramURL}/index.html",
    }
    return url["baseURL"] + url["subURL"] + url["extendedURL"]


def splitIntoBatches(searchParams: list[str], paramsLength: int):
    if REDIS_MAX_CLIENTS is not None:
        batch_size = int(REDIS_MAX_CLIENTS)
        print(f"Batch Size: {batch_size}")
        batches: list[list[str]] = []
        for i in range(0, paramsLength, batch_size):
            batches.append(searchParams[i : i + batch_size])
        return batches
    return [searchParams]


async def getHTMLContentwithCache(
    searchString: str,
    searchParam: str,
    client: ClientSession,
    redis_instance: Redis,
):
    if searchParam != "":
        if searchParam in searchParamURL:
            url = getWebsiteUrl(searchParamURL[searchParam])
            try:
                cachedPage: str = await redis_instance.get(url)
            except:
                raise RedisRequestError(f"Error retrieving HTML for {url} from cache")
            else:
                if cachedPage is not None and isinstance(cachedPage, str):
                    # print("Retrieved from cache")
                    try:
                        parsed = LexborHTMLParser(cachedPage)
                    except:
                        raise ParsingError(f"Error parsing HTML from {url}")
                    else:
                        return await bookParser(searchString, url, parsed)
                else:
                    # print("Retrieved from website")
                    try:
                        async with client.get(url) as response:
                            html_text = await response.text()
                    except:
                        raise HTTPRequestError(f"Error retrieving HTML from {url}")
                    else:
                        try:
                            await redis_instance.set(url, html_text, ex=7200)
                        except:
                            raise RedisRequestError(f"Error caching HTML for {url}")
                        finally:
                            try:
                                parsed = LexborHTMLParser(html_text)
                            except:
                                raise ParsingError(f"Error parsing HTML from {url}")
                            else:
                                return await bookParser(searchString, url, parsed)

    emptyList: list[scrapedProductSchema] = []
    await asyncio.sleep(0)
    return emptyList


async def getHTMLContentnoCache(
    searchString: str,
    searchParam: str,
    client: ClientSession,
):
    if searchParam != "":
        if searchParam in searchParamURL:
            url = getWebsiteUrl(searchParamURL[searchParam])
            try:
                async with client.get(url) as response:
                    html_text = await response.text()
            except:
                raise HTTPRequestError(f"Error retrieving HTML from {url}")
            else:
                try:
                    parsed = LexborHTMLParser(html_text)
                except:
                    raise ParsingError(f"Error parsing HTML from {url}")
                else:
                    return await bookParser(searchString, url, parsed)

    await asyncio.sleep(0)
    emptyList: list[scrapedProductSchema] = []
    return emptyList


async def batchScrape(searchString: str, paramBatch: list[str], client: ClientSession):
    results: list[scrapedProductSchema] = []
    batchLength = len(paramBatch)

    redis_instance = await createRedisInstance(False)
    if isinstance(redis_instance, Redis):
        scrape_tasks = [
            getHTMLContentwithCache(searchString, paramBatch[i], client, redis_instance)
            for i in range(batchLength)
        ]
    else:
        scrape_tasks = [
            getHTMLContentnoCache(searchString, paramBatch[i], client)
            for i in range(batchLength)
        ]
    for results_future in asyncio.as_completed(scrape_tasks):
        result = await results_future
        if result is not None:
            results.extend(result)
    if isinstance(redis_instance, Redis):
        await redis_instance.close()
    return results
