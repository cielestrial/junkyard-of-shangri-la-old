from fastapi import FastAPI, Request  # ,Depends, Form, status
from starlette.templating import Jinja2Templates

from bookScraper import initializeDriver, scrapedProductTemplate, scraper
from helperFunctions import *

# from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")

app = FastAPI()
webDriver = {"driver": initializeDriver()}


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.post("/search")
async def scrape(request: Request):
    url = ""
    results = []
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
                results += scraper(targets[0], url, webDriver["driver"])
    total = len(results)
    print(results)
    return templates.TemplateResponse(
        "results.html", {"request": request, "results": results, "total": total}
    )
