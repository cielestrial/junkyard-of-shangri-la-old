import os

import uvicorn
from aiohttp import ClientSession
from api.mySchemas import (
    MessageSchema,
    MyTimeoutError,
    RedisConnectionError,
    promoSchema,
    scrapedProductSchema,
    scrapedProductsSchema,
    searchSchema,
)
from api.myUtils import batchScrape, createRedisInstance, monitor, splitIntoBatches
from fastapi import Body, FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from redis.asyncio import StrictRedis

ENV = os.getenv("ENV")
frontend = (
    "https://junkyard-of-shangri-la.onrender.com"
    if ENV == "production"
    else "http://localhost:3000"
)
backend = (
    "https://scraper-of-shangri-la.onrender.com"
    if ENV == "production"
    else "http://127.0.0.1:8000"
)

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
    async def _ping():
        response.status_code = 200
        return MessageSchema(status_code=response.status_code, details="pong")

    try:
        return await monitor(_ping())
    except Exception as err:
        response.status_code = 504
        return MessageSchema(status_code=response.status_code, details=f"{err}")


@app.get("/clear")
async def clear_cache(response: Response) -> MessageSchema:
    try:
        filter_key = "http"
        redis_instance = await createRedisInstance()
        if not isinstance(redis_instance, StrictRedis):
            message = "Error clearing cache"
            print(message)
            raise RedisConnectionError(message)

        async def _clear_cache():
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
            print(message)
            response.status_code = 200
            return MessageSchema(status_code=response.status_code, details=message)

        return await monitor(_clear_cache(), redis_instance)

    except (MyTimeoutError, Exception) as err:
        if isinstance(err, MyTimeoutError):
            response.status_code = 504
        else:
            response.status_code = 500
        return MessageSchema(status_code=response.status_code, details=f"{err}")


@app.post("/search")
async def search_scrape(
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
                    if isinstance(batch_results, list):
                        results.extend(batch_results)
            await client.close()

        # print(f"\nResults:\n{results}\n")
        total = len(results)

    except (MyTimeoutError, Exception) as err:
        if isinstance(err, MyTimeoutError):
            response.status_code = 504
        else:
            response.status_code = 500
        return MessageSchema(status_code=response.status_code, details=f"{err}")
    else:
        response.status_code = 200
        return scrapedProductsSchema(
            status_code=response.status_code, total=total, results=results
        )


@app.post("/promo")
async def promo_scrape(
    response: Response,
    promoRequest: promoSchema = Body(...),
) -> scrapedProductsSchema | MessageSchema:
    try:
        # print(f"\nSearch:\n{searchRequest}\n")
        promoParams = promoRequest.promoParams
        paramsLength = len(promoParams)
        results: list[scrapedProductSchema] = []

        if paramsLength > 0:
            batches = splitIntoBatches(promoParams, paramsLength)
            headers = {"Content-Type": "text/html"}
            async with ClientSession(headers=headers) as client:
                for batch in batches:
                    batch_results = await batchScrape("", batch, client)
                    if isinstance(batch_results, list):
                        results.extend(batch_results)
            await client.close()

        # print(f"\nResults:\n{results}\n")
        total = len(results)

    except (MyTimeoutError, Exception) as err:
        if isinstance(err, MyTimeoutError):
            response.status_code = 504
        else:
            response.status_code = 500
        return MessageSchema(status_code=response.status_code, details=f"{err}")
    else:
        response.status_code = 200
        return scrapedProductsSchema(
            status_code=response.status_code, total=total, results=results
        )


if ENV != "production" and __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8000)))
