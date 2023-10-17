from aiohttp import ClientSession
from myErrors import *
from myParser import *
from redis.asyncio import Redis


async def getHTMLContent(
    searchString: str,
    searchParam: str,
    url: str,
    client: ClientSession,
    redis_instance: Redis | None = None,
):
    if searchParam != "":
        if searchParam in searchParamURL:
            if url == "":
                url = getWebsiteUrl(searchParamURL[searchParam])
            try:
                cachedPage: str | None
                if redis_instance is not None:
                    cachedPage = await redis_instance.get(url)
                else:
                    cachedPage = None
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
                        return await bookParser(
                            searchString,
                            searchParam,
                            url,
                            parsed,
                            client,
                            redis_instance,
                        )
                else:
                    # print("Retrieved from website")
                    try:
                        async with client.get(url) as response:
                            html_text = await response.text()
                    except:
                        raise HTTPRequestError(f"Error retrieving HTML from {url}")
                    else:
                        try:
                            if redis_instance is not None:
                                await redis_instance.set(url, html_text, ex=7200)
                        except:
                            raise RedisRequestError(f"Error caching HTML for {url}")
                        finally:
                            try:
                                parsed = LexborHTMLParser(html_text)
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

    emptyList: list[scrapedProductSchema] = []
    await asyncio.sleep(0)
    return emptyList


async def bookParser(
    name: str,
    category: str,
    url: str,
    parsed_HTML: LexborHTMLParser,
    client: ClientSession,
    redis_instance: Redis | None = None,
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
