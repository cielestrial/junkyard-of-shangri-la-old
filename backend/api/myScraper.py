import asyncio

from aiohttp import ClientSession
from api.myParser import getNextPage, getProduct, getWebsiteUrl
from api.mySchemas import (
    HTTPRequestError,
    ParsingError,
    RedisRequestError,
    scrapedProductSchema,
    searchParamURL,
)
from redis.asyncio import StrictRedis
from selectolax.lexbor import LexborHTMLParser, LexborNode


async def getHTMLContent(
    searchString: str,
    searchParam: str,
    url: str,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    if searchParam != "":
        if searchParam in searchParamURL:
            if url == "":
                url = getWebsiteUrl(searchParamURL[searchParam])
            try:
                cachedPage: str | None = None
                if redis_instance is not None:
                    cachedPage = await redis_instance.get(url)
                if cachedPage is None or not isinstance(cachedPage, str):
                    raise RedisRequestError(
                        f"Error retrieving HTML for {url} from cache"
                    )
            except Exception as err:
                print(f"{err}")
                return await requestHTMLContent(
                    searchString, searchParam, url, client, redis_instance
                )
            else:
                # print("Retrieved from cache")
                return await parseHTMLContent(
                    cachedPage, searchString, searchParam, url, client, redis_instance
                )

    emptyList: list[scrapedProductSchema] = []
    return emptyList


async def requestHTMLContent(
    searchString: str,
    searchParam: str,
    url: str,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    try:
        async with client.get(url) as response:
            html_text = await response.text()
    except:
        raise HTTPRequestError(f"Error retrieving HTML from {url}")
    else:
        # print("Retrieved from website")
        try:
            if redis_instance is not None:
                await redis_instance.set(url, html_text, ex=7200)
        except:
            print(f"Error caching HTML for {url}")
        finally:
            return await parseHTMLContent(
                html_text, searchString, searchParam, url, client, redis_instance
            )


async def parseHTMLContent(
    content: str,
    searchString: str,
    searchParam: str,
    url: str,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    try:
        parsed = LexborHTMLParser(content)
    except:
        raise ParsingError(f"Error parsing HTML from {url}")
    else:
        return await bookParser(
            searchString,
            searchParam,
            url,
            parsed,
            client,
            redis_instance,
        )


async def bookParser(
    name: str,
    category: str,
    url: str,
    parsed_HTML: LexborHTMLParser,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    results: list[scrapedProductSchema] = []
    products: list[LexborNode] = []
    if name == "":
        product = parsed_HTML.css_first("article.product_pod")
        if product is None:
            return results
        else:
            products = [product]
    else:
        products = parsed_HTML.css("article.product_pod")
    parse_tasks = [getProduct(product, name, category, url) for product in products]
    for parse_future in asyncio.as_completed(parse_tasks):
        parsed_product = await parse_future
        if parsed_product is not None:
            results.append(parsed_product)
    if name != "":
        next_page = getNextPage(url, parsed_HTML)
        if next_page != "":
            # print(getNextPage.__name__ + " " + next_page)
            result = await getHTMLContent(
                name, category, next_page, client, redis_instance
            )
            if isinstance(result, list):
                results.extend(result)
    return results
