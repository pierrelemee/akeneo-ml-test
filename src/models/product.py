from typing import List, Optional

from pydantic import BaseModel


class Field(BaseModel):
    name: str
    multiple: bool
    label: str
    options: Optional[List[str]] = None
    type: str
