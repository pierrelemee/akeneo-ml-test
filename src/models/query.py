from typing import List

from pydantic import BaseModel

from src.models.llms import LLMType


class ProductFieldsLookupQuery(BaseModel):
    description: str
    llm: LLMType = LLMType.camellm
    fields: List[str]
