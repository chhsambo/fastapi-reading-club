from typing import List
from typing import Annotated
from enum import Enum

from fastapi import FastAPI, Query
from scalar_fastapi import get_scalar_api_reference

from app.schemas.book import Book, BookType, BookCover
from app.schemas.filter import FilterParams
from app.seed_data import generate_books

app = FastAPI(title="Reading Club")


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_books_db: List[Book] = [generate_books() for _ in range(20)]


@app.get("/")
def home():
    return {"Hello": "World!"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/books")
def list_books(
    skip: int = 0,
    limit: int = 10,
    q: Annotated[str | None, Query(min_length=3, max_length=20)] = None,
):
    books = fake_books_db

    if q:
        books = [book for book in books if q in book.title]

    return books[skip : skip + limit]


@app.get("/books/{book_type}")
def read_book(book_type: BookType):
    if book_type is BookType.fiction:
        return {"book_type": book_type, "message": "Here's your fiction book"}

    if book_type.value == "non_fiction":
        return {"book_type": book_type, "message": "Here's your non-fiction book"}

    return {"book_type": book_type, "message": "Here's your drama book"}


@app.get("/books/filter")
def filter_books(filter_params: Annotated[FilterParams, Query()]):
    return filter_params


@app.get("/books/{book_id}")
def read_book(book_id: int, q: str | None = None):
    return {"book_id": book_id, "q": q}


@app.post("/books/")
def create_book(book: Book):
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    results = {"book_id": book_id, "book": book}
    return results


@app.post("/books/images/multiple/")
def create_multiple_books(images: list[BookCover]):
    for image in images:
        print(image.url)
        print(image.source)
    return {"image_count": len(images)}


@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name is ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    if model_name is ModelName.resnet:
        return {"model_name": model_name, "message": "Have some residuals"}

    return {"model_name": model_name, "message": "New model found!"}
