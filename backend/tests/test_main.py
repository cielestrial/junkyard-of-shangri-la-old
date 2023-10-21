import sys
from unicodedata import category

from api.mySchemas import MessageSchema, scrapedProductsSchema
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from main import app

sys.path.append("api")

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    encoded_mesage = jsonable_encoder(MessageSchema(status_code=200, details="pong"))
    assert response.json() == encoded_mesage


def test_promo():
    promoRequest = jsonable_encoder(
        {
            "promoParams": [
                "Crime",
                "Fantasy",
                "Fiction",
            ]
        }
    )
    response = client.post(
        "/promo",
        json=promoRequest,
    )
    assert response.status_code == 200

    assert response.json()["total"] == 3


def test_search():
    searchRequest = jsonable_encoder(
        {
            "searchString": "The",
            "searchParams": [
                "Crime",
                "Fantasy",
                "Fiction",
            ],
        }
    )
    response = client.post(
        "/search",
        json=searchRequest,
    )
    assert response.status_code == 200

    assert response.json()["total"] == 55
