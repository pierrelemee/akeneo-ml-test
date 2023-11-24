from typing import List

from pydantic import BaseModel

from src.models.llms import LLMType


class ProductFieldsLookupQuery(BaseModel):
    description: str
    llm: LLMType = LLMType.CAMELLM
    fields: List[str]
