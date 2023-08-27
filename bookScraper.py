from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


class scrapedProductTemplate:
    """
    Has the following properties: image, name, price, status, and link.
    The values of these properties are all of type(str).
    """

    image: str
    name: str
    price: str
    status: str
    link: str


def initializeDriver():
    options = webdriver.FirefoxOptions()
    options.add_argument("-headless")
    return webdriver.Firefox(options=options)


def getHtmlContent(url: str, driver: WebDriver):
    driver.get(url)
    content = driver.page_source
    driver.close()
    return BeautifulSoup(content, "lxml")


def getImage(product: Tag):
    image = product.findChild("img", attrs={"src": True}, recursive=True)
    if isinstance(image, Tag):
        src = image["src"]
        if isinstance(src, str):
            return src.strip()
        else:
            raise TypeError("src must be of type(str)")
    else:
        raise TypeError("image must be of type(Tag)")


def getName(product: Tag):
    name = product.findChild("a", attrs={"title": True}, recursive=True)
    if isinstance(name, Tag):
        title = name["title"]
        if isinstance(title, str):
            return title.strip()
        else:
            raise TypeError("title must be of type(str)")
    else:
        raise TypeError("name must be of type(Tag)")


def getPrice(product: Tag):
    price = product.findChild("p", attrs={"class": "price_color"}, recursive=True)
    if isinstance(price, Tag):
        return price.text.strip()
    else:
        raise TypeError("price must be of type(Tag)")


def getStatus(product: Tag):
    status = product.findChild("p", attrs={"class": "availability"}, recursive=True)
    if isinstance(status, Tag):
        return status.text.strip()
    else:
        raise TypeError("status must be of type(Tag)")


def getLink(product: Tag):
    link = product.findChild("a", attrs={"href": True}, recursive=True)
    if isinstance(link, Tag):
        href = link["href"]
        if isinstance(href, str):
            return href.strip()
        else:
            raise TypeError("href must be of type(str)")
    else:
        raise TypeError("link must be of type(Tag)")


def scraper(name: str, url: str, driver: WebDriver):
    soup = getHtmlContent(url, driver)
    products: list[Tag] = soup.find_all("article", attrs={"class": "product_pod"})
    results: list[scrapedProductTemplate] = []

    for product in products:
        scrapedProduct = scrapedProductTemplate()
        productName = getName(product)
        if name not in productName.casefold():
            print(productName.casefold())
            continue
        status = getStatus(product)
        if "In" not in status.title():
            continue
        else:
            scrapedProduct.name = productName
            scrapedProduct.image = url + getImage(product)
            scrapedProduct.price = getPrice(product)
            scrapedProduct.status = status
            scrapedProduct.link = url + getLink(product)
            results.append(scrapedProduct)

    return results


testCase = "T"
tester = scraper(testCase, "http://books.toscrape.com/", initializeDriver())
for x in tester:
    print(x)

# going to display data on our html page
