import databases
import ormar
import sqlalchemy
from pydantic import HttpUrl, field_validator

from .config import settings

database = databases.Database(settings.DATABASE_URL)
metadata = sqlalchemy.MetaData()


class UserTable(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        database=database,
        metadata=metadata,
        tablename="users",
    )

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)


class BookTable(ormar.Model):
    ormar_config = ormar.OrmarConfig(
        database=database,
        metadata=metadata,
        tablename="books",
    )

    id: int = ormar.Integer(primary_key=True)
    title: str = ormar.String(max_length=100)
    subtitle: str = ormar.String(max_length=300, nullable=True, default=None)
    author: str = ormar.String(max_length=100, nullable=True, default=None)
    publisher: str = ormar.String(max_length=100, nullable=True, default=None)
    price_khr: int = ormar.Integer(nullable=True, default=None, minimum=1000, maximum=999999)
    price_usd: float = ormar.Float(nullable=True, default=None, minimum=0.25, maximum=250)
    is_offer: bool = ormar.Boolean(nullable=True, default=None)
    tags: set[str] = ormar.JSON(default=set())
    cover_image: str = ormar.String(max_length=250)

    # Validators
    @field_validator('cover_image')
    def validate_cover_image(cls, v):
        return HttpUrl(v) if v else None

    @field_validator('price_khr')
    def validate_price_khr(cls, v):
        if v is not None and (v < 1000 or v >= 1_000_000):
            raise ValueError("price_khr must be ≥1000 and <1,000,000")
        return v

    @field_validator('price_usd')
    def validate_price_usd(cls, v):
        if v is not None and (v < 0.25 or v >= 250):
            raise ValueError("price_usd must be ≥0.25 and <250")
        return v

    @field_validator('tags')
    def validate_tags(cls, v):
        if isinstance(v, list):
            return set(v)
        elif isinstance(v, set):
            return v
        raise ValueError("Tags must be a set or list")


engine = sqlalchemy.create_engine(settings.DATABASE_URL)
metadata.create_all(engine)