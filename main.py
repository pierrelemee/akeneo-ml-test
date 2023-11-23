from typing import Annotated

from fastapi import FastAPI, Depends

from src.dtos import ProductFieldsQueryDTO, LLMType
from src.fields import FieldManager
from src.llms import AbstractLLM, LLaMA, CameLLM

app = FastAPI()


async def get_llama2():
    return LLaMA()


async def get_camellm():
    return CameLLM()


@app.post("/api/product/fields/lookup")
async def index(
    query: ProductFieldsQueryDTO,
    field_manager: Annotated[FieldManager, Depends(FieldManager)],
    llama2: Annotated[AbstractLLM, Depends(get_llama2)],
    camellm: Annotated[AbstractLLM, Depends(get_camellm)],
):
    res = {}
    llm = llama2 if query.llm == LLMType.llama2 else camellm
    for field in query.fields:
        if (target := field_manager.get_field(field)) is not None:
            res[field] = llm.lookup_field_description(target, query.description)
        else:
            res[field] = None

    return res
