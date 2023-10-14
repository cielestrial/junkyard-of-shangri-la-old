import asyncio
from urllib.parse import urljoin

from selectolax.lexbor import LexborHTMLParser, LexborNode
from src.mySchemas import *


def getWebsiteUrl(paramURL: str):
    """Returns the url for the provided domain name."""
    url = {
        "baseURL": "https://books.toscrape.com/",
        "subURL": "catalogue/",
        "extendedURL": f"category/books/{paramURL}/index.html",
    }
    return url["baseURL"] + url["subURL"] + url["extendedURL"]


async def getProduct(product: LexborNode, name: str, category: str, url: str):
    scrapedProduct = scrapedProductSchema(
        image="", name="", price="", status="", category=category, link=""
    )
    scrapedProduct.name = getName(product)
    if name == "":
        name = scrapedProduct.name
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


def getNextPage(url: str, parsed_HTML: LexborHTMLParser):
    next_page = parsed_HTML.css_first("li.next a[href]")
    if next_page is not None:
        href = next_page.attributes["href"]
        if isinstance(href, str):
            return urljoin(url, href)
        else:
            raise TypeError("href must be of type(str)")
    else:
        return ""
