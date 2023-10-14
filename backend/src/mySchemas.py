from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    status_code: int = Field(examples=[200])
    details: str = Field(examples=["Hello World!"])


class scrapedProductSchema(BaseModel):
    """
    Has the following properties: image, name, price, status, and link.
    The values of these properties are all of type(str).
    """

    image: str = Field(
        examples=[
            "https://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg"
        ]
    )
    name: str = Field(examples=["A Light in the Attic"])
    price: str = Field(examples=["£51.77"])
    status: str = Field(examples=["In stock"])
    category: str = Field(examples=["Poetry"])
    link: str = Field(
        examples=[
            "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
        ]
    )

    def __str__(self):
        return f"{self.name}, {self.status}, {self.price}, {self.category}"


class scrapedProductsSchema(BaseModel):
    status_code: int = Field(examples=[200])
    total: int = Field(examples=[1])
    results: list[scrapedProductSchema]


class promoSchema(BaseModel):
    promoParams: list[str] = Field(
        examples=[
            [
                "Crime",
                "Fantasy",
                "Fiction",
                "Mystery",
                "Nonfiction",
                "Philosophy",
                "Romance",
                "Science Fiction",
                "Self Help",
                "Short Stories",
            ]
        ]
    )


class searchSchema(BaseModel):
    searchString: str = Field(examples=["The Attic"])
    searchParams: list[str] = Field(
        examples=[
            [
                "Crime",
                "Fantasy",
                "Fiction",
                "Mystery",
                "Nonfiction",
                "Philosophy",
                "Romance",
                "Science Fiction",
                "Self Help",
                "Short Stories",
            ]
        ]
    )


searchParamURL = {
    "Travel": "travel_2",
    "Mystery": "mystery_3",
    "Historical Fiction": "historical-fiction_4",
    "Sequential Art": "sequential-art_5",
    "Classics": "classics_6",
    "Philosophy": "philosophy_7",
    "Romance": "romance_8",
    "Womens Fiction": "womens-fiction_9",
    "Fiction": "fiction_10",
    "Childrens": "childrens_11",
    "Religion": "religion_12",
    "Nonfiction": "nonfiction_13",
    "Music": "music_14",
    "Default": "default_15",
    "Science Fiction": "science-fiction_16",
    "Sports and Games": "sports-and-games_17",
    "Add a comment": "add-a-comment_18",
    "Fantasy": "fantasy_19",
    "New Adult": "new-adult_20",
    "Young Adult": "young-adult_21",
    "Science": "science_22",
    "Poetry": "poetry_23",
    "Paranormal": "paranormal_24",
    "Art": "art_25",
    "Psychology": "psychology_26",
    "Autobiography": "autobiography_27",
    "Parenting": "parenting_28",
    "Adult Fiction": "adult-fiction_29",
    "Humor": "humor_30",
    "Horror": "horror_31",
    "History": "history_32",
    "Food and Drink": "food-and-drink_33",
    "Christian Fiction": "christian-fiction_34",
    "Business": "business_35",
    "Biography": "biography_36",
    "Thriller": "thriller_37",
    "Contemporary": "contemporary_38",
    "Spirituality": "spirituality_39",
    "Academic": "academic_40",
    "Self Help": "self-help_41",
    "Historical": "historical_42",
    "Christian": "christian_43",
    "Suspense": "suspense_44",
    "Short Stories": "short-stories_45",
    "Novels": "novels_46",
    "Health": "health_47",
    "Politics": "politics_48",
    "Cultural": "cultural_49",
    "Erotica": "erotica_50",
    "Crime": "crime_51",
}
