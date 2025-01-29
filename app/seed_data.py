from faker import Faker
from app.schemas.book import Book

fake = Faker()


def generate_books() -> Book:
    return Book(
        title=fake.sentence(nb_words=3),
        subtitle=fake.sentence(nb_words=5) if fake.boolean() else None,
        author=fake.name(),
        publisher=fake.company() if fake.boolean() else None,
        price_khr=fake.random_int(min=1000, max=100000) if fake.boolean() else None,
        price_usd=fake.random_number(digits=2) if fake.boolean() else None,
        is_offer=fake.boolean() if fake.boolean() else None
    )
