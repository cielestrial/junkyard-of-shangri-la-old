import asyncio

from aiohttp import ClientSession
from .my_parser import get_next_page, get_product, get_website_url
from .my_schemas import (
    HTTPRequestError,
    ParsingError,
    RedisRequestError,
    ScrapedProductSchema,
    search_param_url,
)
from redis.asyncio import StrictRedis
from selectolax.lexbor import LexborHTMLParser, LexborNode


async def get_html_content(
    search_string: str,
    search_param: str,
    url: str,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    if search_param != "":
        if search_param in search_param_url:
            if url == "":
                url = get_website_url(search_param_url[search_param])
            try:
                cached_page: str | None = None
                if redis_instance is not None:
                    cached_page = await redis_instance.get(url)
                if cached_page is None or not isinstance(cached_page, str):
                    raise RedisRequestError(
                        f"Error retrieving HTML for {url} from cache"
                    )
            except Exception as err:
                print(f"{err}")
                return await request_html_content(
                    search_string, search_param, url, client, redis_instance
                )
            else:
                # print("Retrieved from cache")
                return await parse_html_content(
                    cached_page,
                    search_string,
                    search_param,
                    url,
                    client,
                    redis_instance,
                )

    empty_list: list[ScrapedProductSchema] = []
    return empty_list


async def request_html_content(
    search_string: str,
    search_param: str,
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
            return await parse_html_content(
                html_text, search_string, search_param, url, client, redis_instance
            )


async def parse_html_content(
    content: str,
    search_string: str,
    search_param: str,
    url: str,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    try:
        parsed = LexborHTMLParser(content)
    except:
        raise ParsingError(f"Error parsing HTML from {url}")
    else:
        return await book_parser(
            search_string,
            search_param,
            url,
            parsed,
            client,
            redis_instance,
        )


async def book_parser(
    name: str,
    category: str,
    url: str,
    parsed_html: LexborHTMLParser,
    client: ClientSession,
    redis_instance: StrictRedis | None = None,
):
    results: list[ScrapedProductSchema] = []
    products: list[LexborNode] = []
    if name == "":
        product = parsed_html.css_first("article.product_pod")
        if product is None:
            return results
        else:
            products = [product]
    else:
        products = parsed_html.css("article.product_pod")
    parse_tasks = [get_product(product, name, category, url) for product in products]
    for parse_future in asyncio.as_completed(parse_tasks):
        parsed_product = await parse_future
        if parsed_product is not None:
            results.append(parsed_product)
    if name != "":
        next_page = get_next_page(url, parsed_html)
        if next_page != "":
            # print(get_next_page.__name__ + " " + next_page)
            result = await get_html_content(
                name, category, next_page, client, redis_instance
            )
            if isinstance(result, list):
                results.extend(result)
    return results
