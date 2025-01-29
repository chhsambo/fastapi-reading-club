from typing import  Literal
from pydantic import BaseModel, Field

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}
    
    limit: int = Field(10, gt=0, le=100, description="Number of books to return")
    offset: int = Field(0, ge=0, description="Number of books to skip")
    order_by: Literal["created_at", "updated_at"] = Field("created_at", description="Order by created_at or updated_at")
    tags: list[str] = []