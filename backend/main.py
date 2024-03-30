import os

import uvicorn
from aiohttp import ClientSession
from api.my_schemas import (
    MessageSchema,
    MyTimeoutError,
    RedisConnectionError,
    PromoSchema,
    ScrapedProductSchema,
    ScrapedProductsSchema,
    SearchSchema,
)
from api.my_utils import (
    batch_scrape,
    create_redis_instance,
    monitor,
    split_into_batches,
)
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
        redis_instance = await create_redis_instance()
        if not isinstance(redis_instance, StrictRedis):
            message = "Error clearing cache"
            print(message)
            raise RedisConnectionError(message)

        async def _clear_cache():
            all_keys: list[str] = (await redis_instance.scan(0))[1]
            junkyard_keys: list[str] = [key for key in all_keys if filter_key in key]
            print(f"All Keys:{junkyard_keys}")

            while len(junkyard_keys) > 0:
                await redis_instance.delete(*junkyard_keys)
                all_keys = (await redis_instance.scan(0))[1]
                junkyard_keys = [key for key in all_keys if filter_key in key]

            await redis_instance.close()
            print(f"All Keys:{junkyard_keys}")
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
    search_request: SearchSchema = Body(...),
) -> ScrapedProductsSchema | MessageSchema:
    try:
        # print(f"\nSearch:\n{search_request}\n")
        search_string = search_request.searchString
        search_params = search_request.searchParams
        param_length = len(search_params)
        results: list[ScrapedProductSchema] = []

        if search_string != "" and param_length > 0:
            batches = split_into_batches(search_params, param_length)
            headers = {"Content-Type": "text/html"}
            async with ClientSession(headers=headers) as client:
                for batch in batches:
                    batch_results = await batch_scrape(search_string, batch, client)
                    if isinstance(batch_results, list):
                        results.extend(batch_results)

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
        return ScrapedProductsSchema(
            status_code=response.status_code, total=total, results=results
        )


@app.post("/promo")
async def promo_scrape(
    response: Response,
    promo_request: PromoSchema = Body(...),
) -> ScrapedProductsSchema | MessageSchema:
    try:
        # print(f"\nPromo:\n{promo_request}\n")
        promo_params = promo_request.promoParams
        param_length = len(promo_params)
        results: list[ScrapedProductSchema] = []

        if param_length > 0:
            batches = split_into_batches(promo_params, param_length)
            headers = {"Content-Type": "text/html"}
            async with ClientSession(headers=headers) as client:
                for batch in batches:
                    batch_results = await batch_scrape("", batch, client)
                    if isinstance(batch_results, list):
                        results.extend(batch_results)

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
        return ScrapedProductsSchema(
            status_code=response.status_code, total=total, results=results
        )


if ENV != "production" and __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(os.environ.get("PORT", 8000)))
