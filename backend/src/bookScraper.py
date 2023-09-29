import asyncio
from urllib.parse import urljoin

from selectolax.lexbor import LexborHTMLParser, LexborNode
from src.schemas import *


async def bookParser(name: str, category: str, url: str, parsed_HTML: LexborHTMLParser):
    results: list[scrapedProductSchema] = []
    products = parsed_HTML.css("article.product_pod")
    parse_tasks = [scrapeProduct(product, name, category, url) for product in products]
    for parse_future in asyncio.as_completed(parse_tasks):
        parsed_product = await parse_future
        if parsed_product is not None:
            results.append(parsed_product)
    return results


async def scrapeProduct(product: LexborNode, name: str, category: str, url: str):
    scrapedProduct = scrapedProductSchema(
        image="", name="", price="", status="", category=category, link=""
    )
    scrapedProduct.name = getName(product)
    if name.casefold() in scrapedProduct.name.casefold():
        scrapedProduct.status = getStatus(product)
        if "In" in scrapedProduct.status.title():
            async with asyncio.TaskGroup() as tg:
                tg.create_task(getPrice(product, scrapedProduct))
                tg.create_task(getImage(product, scrapedProduct, url))
                tg.create_task(getLink(product, scrapedProduct, url))
            # print(f"product: {scrapedProduct}")
            return scrapedProduct


def getName(product: LexborNode):
    name = product.css_first("h3 a[title]")
    if name is not None:
        title = name.attributes["title"]
        if isinstance(title, str):
            return title.strip()
        else:
            raise TypeError("title must be of type(str)")
    else:
        return ""


def getStatus(product: LexborNode):
    status = product.css_first("p.availability")
    if status is not None:
        return status.text(deep=True, strip=True)
    else:
        return ""


async def getPrice(product: LexborNode, scrapedProduct: scrapedProductSchema):
    price = product.css_first("p.price_color")
    if price is not None:
        scrapedProduct.price = price.text(deep=True, strip=True)
    else:
        return ""


async def getImage(product: LexborNode, scrapedProduct: scrapedProductSchema, url: str):
    image = product.css_first("img[src]")
    if image is not None:
        src = image.attributes["src"]
        if isinstance(src, str):
            scrapedProduct.image = urljoin(url, src)
        else:
            raise TypeError("src must be of type(str)")
    else:
        return ""


async def getLink(product: LexborNode, scrapedProduct: scrapedProductSchema, url: str):
    link = product.css_first("a[href]")
    if link is not None:
        href = link.attributes["href"]
        if isinstance(href, str):
            scrapedProduct.link = urljoin(url, href)
        else:
            raise TypeError("href must be of type(str)")
    else:
        return ""
