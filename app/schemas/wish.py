from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class WishBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    link: Optional[HttpUrl] = None
    price_estimate: Optional[float] = Field(default=None, ge=0)
    notes: Optional[str] = None


class WishCreate(WishBase):
    pass


class WishUpdate(WishBase):
    pass


class WishOut(WishBase):
    id: int
    owner_id: int
