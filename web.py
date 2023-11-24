import os
import importlib

from typing import Annotated

from fastapi import FastAPI, Depends

from src.models.query import ProductFieldsLookupQuery
from src.models.llms import LLMType
from src.services.field import FieldManager
from src.models.llms import AbstractLLM


config = importlib.import_module(os.getenv("CONFIG_MODULE", "config.example"))

print(config)

if not hasattr(config, "get_llama2") or not callable(config.get_llama2):
    raise Exception("Missing configuration for llama2")

if not hasattr(config, "get_camellm") or not callable(config.get_camellm):
    raise Exception("Missing configuration for camellm")


app = FastAPI()


@app.post("/api/product/fields/lookup")
async def index(
    query: ProductFieldsLookupQuery,
    field_manager: Annotated[FieldManager, Depends(FieldManager)],
    llama2: Annotated[AbstractLLM, Depends(config.get_llama2)],
    camellm: Annotated[AbstractLLM, Depends(config.get_camellm)],
):
    res = {}
    llm = llama2 if query.llm == LLMType.LLAMA else camellm
    for field in query.fields:
        if (target := field_manager.get_field(field)) is not None:
            res[field] = llm.lookup_field_description(target, query.description)
        else:
            res[field] = None

    return res
