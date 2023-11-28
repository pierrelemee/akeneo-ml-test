import os
import importlib

from typing import Annotated

from fastapi import FastAPI, Depends

from src.dtos.query import ProductFieldsLookupQuery
from src.llm.llms import LLMType
from src.services.product import ProductLookupManager

config = importlib.import_module(os.getenv("CONFIG_MODULE", "config.example"))

if not hasattr(config, "get_llama2") or not callable(config.get_llama2):
    raise Exception("Missing configuration for llama2")

if not hasattr(config, "get_camellm") or not callable(config.get_camellm):
    raise Exception("Missing configuration for camellm")


app = FastAPI()


@app.post("/api/product/fields/lookup")
async def index(
    query: ProductFieldsLookupQuery,
    product_lookup_manager: Annotated[
        ProductLookupManager, Depends(ProductLookupManager)
    ],
):
    get_llm = config.get_llama2 if query.llm == LLMType.LLAMA else config.get_camellm

    return product_lookup_manager.lookup_product_fields(query, get_llm)
