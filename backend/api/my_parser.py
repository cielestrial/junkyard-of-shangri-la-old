import asyncio
from urllib.parse import urljoin

from .my_schemas import ScrapedProductSchema
from selectolax.lexbor import LexborHTMLParser, LexborNode


def get_website_url(param_url: str):
    """Returns the url for the provided domain name."""
    url = {
        "base_url": "https://books.toscrape.com/",
        "sub_url": "catalogue/",
        "extended_url": f"category/books/{param_url}/index.html",
    }
    return url["base_url"] + url["sub_url"] + url["extended_url"]


async def get_product(product: LexborNode, name: str, category: str, url: str):
    scraped_product = ScrapedProductSchema(
        image="", name="", price="", status="", category=category, link=""
    )
    scraped_product.name = get_name(product)
    if name == "":
        name = scraped_product.name
    if name.casefold() in scraped_product.name.casefold():
        scraped_product.status = get_status(product)
        if "In" in scraped_product.status.title():
            async with asyncio.TaskGroup() as tg:
                tg.create_task(get_price(product, scraped_product))
                tg.create_task(get_image(product, scraped_product, url))
                tg.create_task(get_link(product, scraped_product, url))
            # print(f"product: {scraped_product}")
            return scraped_product


def get_name(product: LexborNode):
    name = product.css_first("h3 a[title]")
    if name is not None:
        title = name.attributes["title"]
        if isinstance(title, str):
            return title.strip()
        else:
            raise TypeError("title must be of type(str)")
    else:
        return ""


def get_status(product: LexborNode):
    status = product.css_first("p.availability")
    if status is not None:
        return status.text(deep=True, strip=True)
    else:
        return ""


async def get_price(product: LexborNode, scraped_product: ScrapedProductSchema):
    price = product.css_first("p.price_color")
    if price is not None:
        scraped_product.price = price.text(deep=True, strip=True)
    else:
        return ""


async def get_image(
    product: LexborNode, scraped_product: ScrapedProductSchema, url: str
):
    image = product.css_first("img[src]")
    if image is not None:
        src = image.attributes["src"]
        if isinstance(src, str):
            scraped_product.image = urljoin(url, src)
        else:
            raise TypeError("src must be of type(str)")
    else:
        return ""


async def get_link(
    product: LexborNode, scraped_product: ScrapedProductSchema, url: str
):
    link = product.css_first("a[href]")
    if link is not None:
        href = link.attributes["href"]
        if isinstance(href, str):
            scraped_product.link = urljoin(url, href)
        else:
            raise TypeError("href must be of type(str)")
    else:
        return ""


def get_next_page(url: str, parsed_html: LexborHTMLParser):
    next_page = parsed_html.css_first("li.next a[href]")
    if next_page is not None:
        href = next_page.attributes["href"]
        if isinstance(href, str):
            return urljoin(url, href)
        else:
            raise TypeError("href must be of type(str)")
    else:
        return ""
