from typing import Optional

from sqlmodel import SQLModel, Field


class pokemon(SQLModel, table=True):
    id: int = Field(primary_key=True, nullable=False)
    name: str = Field(nullable=False)
    url: str = Field(nullable=False)

    weight: Optional[int] = Field()
    height: Optional[int] = Field()
    speed: Optional[int] = Field()
