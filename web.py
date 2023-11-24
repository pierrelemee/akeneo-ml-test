import concurrent.futures
import os
import importlib

from typing import Annotated, Optional, Callable

from fastapi import FastAPI, Depends

from src.models.product import Field
from src.models.query import ProductFieldsLookupQuery
from src.models.llms import LLMType, AbstractLLM
from src.services.field import FieldManager

config = importlib.import_module(os.getenv("CONFIG_MODULE", "config.example"))

if not hasattr(config, "get_llama2") or not callable(config.get_llama2):
    raise Exception("Missing configuration for llama2")

if not hasattr(config, "get_camellm") or not callable(config.get_camellm):
    raise Exception("Missing configuration for camellm")


app = FastAPI()


@app.post("/api/product/fields/lookup")
async def index(
    query: ProductFieldsLookupQuery,
    field_manager: Annotated[FieldManager, Depends(FieldManager)],
):
    res = {}
    callback = config.get_llama2 if query.llm == LLMType.LLAMA else config.get_camellm
    fields = {name: field_manager.get_field(name) for name in query.fields}

    async def lookup_function(
        description: str, field: Optional[Field], get_llm: Callable
    ):
        llm: AbstractLLM = await get_llm()
        return (
            field.name,
            llm.lookup_field_description(field, description)
            if isinstance(llm, AbstractLLM)
            else None,
        )

    # Lookup for field value simultaneously (using a ThreadPoolExecutor)
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(query.fields)
    ) as executor:
        futures = []
        for name, field in fields.items():
            if field is None:
                res[name] = None
            else:
                futures.append(
                    executor.submit(
                        lookup_function,
                        description=query.description,
                        field=field,
                        get_llm=callback,
                    )
                )
        for future in concurrent.futures.as_completed(futures, timeout=5):
            name, value = await future.result()
            res[name] = value

    return res
