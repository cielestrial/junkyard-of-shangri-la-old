from fastapi import FastAPI, Request  # ,Depends, Form, status
from starlette.templating import Jinja2Templates

from src.bookScraper import initializeDriver, scrapedProductTemplate, scraper
from src.helperFunctions import *

# from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")

app = FastAPI()


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/search")
async def scrape(request: Request):
    url = ""
    results: list[scrapedProductTemplate] = []
    requestStr = (await request.body()).decode("utf-8")
    print(requestStr)
    targets = cleanupFormInput(requestStr)

    if len(targets) > 1:
        webDriver = {"driver": initializeDriver()}
        for x in range(len(targets) - 1):
            # will need to open multiple browsers
            url = getWebsiteUrl(targets[x + 1])
            if url == "":
                continue
            else:
                results += scraper(targets[0], url, webDriver["driver"])
    total = len(results)
    print("\nResults:\n")
    for y in results:
        print(y)
    return templates.TemplateResponse(
        "results.html", {"request": request, "results": results, "total": total}
    )
