from typing import Annotated

from fastapi import FastAPI, Depends

from src.dtos import ProductFieldsQueryDTO
from src.fields import FieldManager

app = FastAPI()


@app.post("/api/product/fields/lookup")
def index(
    query: ProductFieldsQueryDTO,
    field_manager: Annotated[FieldManager, Depends(FieldManager)],
):
    res = {}
    for field in query.fields:
        if (target := field_manager.get_field(field)) is not None:
            res[field] = target.label
        else:
            res[field] = None

    return res
