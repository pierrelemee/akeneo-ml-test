from typing import List

from pydantic import BaseModel


class ProductFieldsQueryDTO(BaseModel):
    description: str
    llm: str
    fields: List[str]