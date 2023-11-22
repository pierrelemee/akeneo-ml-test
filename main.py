from typing import Union, List, Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from src.fields import FieldManager

app = FastAPI()


class ProductFieldsQueryDTO(BaseModel):
    """
    description: str
    """
    description: str
    llm: str
    fields: List[str]


@app.post("/api/product/fields")
def index(query: ProductFieldsQueryDTO, field_manager: Annotated[FieldManager, Depends(FieldManager)]):
    res = {}
    for field in query.fields:
        if (target := field_manager.get_field(field)) is not None:
            res[field] = target.label
        else:
            res[field] = None

    return res
