from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    message: str = Field(examples=["pong"])


class scrapedProductSchema(BaseModel):
    """
    Has the following properties: image, name, price, status, and link.
    The values of these properties are all of type(str).
    """

    image: str = Field(examples=["http://image"])
    name: str = Field(examples=["The Attic"])
    price: str = Field(examples=["10£"])
    status: str = Field(examples=["In Stock"])
    link: str = Field(examples=["http://link"])

    def __str__(self):
        return f"{self.name}, {self.status}, {self.price}"


class scrapedProductsSchema(BaseModel):
    total: int = Field(examples=[1])
    results: list[scrapedProductSchema]
