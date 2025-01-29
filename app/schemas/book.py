from enum import Enum
from pydantic import BaseModel, Field, HttpUrl


class BookType(str, Enum):
    fiction = "fiction"
    non_fiction = "non-fiction"
    drama = "drama"
    
class BookCover(BaseModel):
    url: HttpUrl
    source: str


class Book(BaseModel):
    title: str = Field(description="The title of the book", max_length=100)
    subtitle: str | None = Field(description="The subtitle of the book", default=None, max_length=300)
    author: str | None = None
    publisher: str | None = None
    price_khr: int | None = Field(description="The price of the book in KHR", default=None, ge=1000, lt=1_000_000)
    price_usd: float | None = Field(description="The price of the book in USD", default=None, ge=0.25, lt=250)
    is_offer: bool | None = None
    tags: set[str] = Field(description="The tags of the book", default=set(), max_items=10)
    cover_image: BookCover | None = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Foo",
                    "subtitle": "A very nice Item",
                    "author": "Sambo",
                    "published": "O'relliy",
                    "price_kh": 35400,
                    "tax_usd": 8.2,
                    "is_offer": True,
                    "tags": ["fiction", "non-fiction"]
                }
            ]
        }
    }
