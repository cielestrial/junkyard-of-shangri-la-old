from fastapi import Body, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from src.utils import *

ENV = os.getenv("ENV")
frontend = "" if ENV == "production" else "http://localhost:3000"
backend = "https://scraper-of-shangri-la.onrender.com" if ENV == "production" else "http://127.0.0.1:8000"

app = FastAPI()

origins = [frontend, backend]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Access-Control-Allow-Headers",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Content-Language",
        "Content-Type",
    ],
)


@app.get("/")
async def redirect_frontend():
    return RedirectResponse(frontend)


@app.get("/api")
@app.get("/docs")
async def redirect_docs():
    return RedirectResponse(backend + "/docs")


@app.get("/ping")
async def ping(response: Response) -> MessageSchema:
    try:
        redis_instance = await createRedisInstance(True)
        if isinstance(redis_instance, Redis):
            await redis_instance.close()
    except Exception as err:
        response.status_code = 500
        return MessageSchema(status_code=500, details=f"{err}")
    else:
        response.status_code = 200
        return MessageSchema(status_code=200, details="pong")


@app.get("/clear")
async def clear_cache(response: Response) -> MessageSchema:
    try:
        filter_key = "http"
        redis_instance = await createRedisInstance(True)
        if isinstance(redis_instance, Redis):
            allKeys: list[str] = (await redis_instance.scan(0))[1]
            junkyardKeys: list[str] = [key for key in allKeys if filter_key in key]
            print(f"All Keys:{junkyardKeys}")

            while len(junkyardKeys) > 0:
                await redis_instance.delete(*junkyardKeys)
                allKeys = (await redis_instance.scan(0))[1]
                junkyardKeys = [key for key in allKeys if filter_key in key]

            await redis_instance.close()
            print(f"All Keys:{junkyardKeys}")
            message = "Cache cleared"
        else:
            message = "Error clearing cache"
        print(message)
    except Exception as err:
        response.status_code = 500
        return MessageSchema(status_code=500, details=f"{err}")
    else:
        response.status_code = 200
        return MessageSchema(status_code=200, details=message)


@app.post("/search")
async def scrape(
    response: Response,
    searchRequest: searchSchema = Body(...),
) -> scrapedProductsSchema | MessageSchema:
    try:
        # print(f"\nSearch:\n{searchRequest}\n")
        searchString = searchRequest.searchString
        searchParams = searchRequest.searchParams
        paramsLength = len(searchParams)
        results: list[scrapedProductSchema] = []

        if searchString != "" and paramsLength > 0:
            batches = splitIntoBatches(searchParams, paramsLength)
            headers = {"Content-Type": "text/html"}
            async with ClientSession(headers=headers) as client:
                for batch in batches:
                    batch_results = await batchScrape(searchString, batch, client)
                    results.extend(batch_results)
            await client.close()

        # print(f"\nResults:\n{results}\n")
        total = len(results)
    except Exception as err:
        response.status_code = 500
        return MessageSchema(status_code=500, details=f"{err}")
    else:
        response.status_code = 200
        return scrapedProductsSchema(status_code=200, total=total, results=results)
