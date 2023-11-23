from enum import Enum
from typing import List

from pydantic import BaseModel


class LLMType(Enum):
    llama2 = "llama2"
    camellm = "camellm"


class ProductFieldsQueryDTO(BaseModel):
    description: str
    llm: LLMType = LLMType.camellm
    fields: List[str]
