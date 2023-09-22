import asyncio

from fastapi import FastAPI, Request  # ,Depends, Form, status
from src.bookScraper import scraper
from src.helperFunctions import *
from src.schemas import MessageSchema, scrapedProductSchema, scrapedProductsSchema
from starlette.templating import Jinja2Templates

# from starlette.responses import RedirectResponse

templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get("/ping")
async def ping() -> MessageSchema:
    await asyncio.sleep(5)
    message = MessageSchema(message="pong")
    return message


@app.post("/search")
async def scrape(request: Request) -> scrapedProductsSchema:
    url = ""
    results: list[scrapedProductSchema] = []
    requestStr = (await request.body()).decode("utf-8")
    print(requestStr)
    targets = cleanupFormInput(requestStr)

    if len(targets) > 1:
        for x in range(len(targets) - 1):
            # will need to open multiple browsers
            url = getWebsiteUrl(targets[x + 1])
            if url == "":
                continue
            else:
                results += scraper(targets[0], url)
    total = len(results)
    print("\nResults:\n")
    for y in results:
        print(y)
    message = scrapedProductsSchema(total=total, results=results)
    return message
