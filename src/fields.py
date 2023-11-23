from typing import List, Dict, Optional
import os

from pydantic import TypeAdapter, BaseModel


class Field(BaseModel):
    name: str
    multiple: bool
    label: str
    options: Optional[List[str]] = None
    type: str


class FieldManager:
    """
    Service class responsible for
    """
    _fields: Dict[str, Field]

    def __init__(self):
        # Load field knowledge base from json file
        # TODO: handle file issues (existence, permission, format)
        with open(self.__get_fields_file_path()) as file:
            self._fields = {field.name: field for field in TypeAdapter(List[Field]).validate_json(file.read())}

    def get_field(self, name: str) -> Optional[Field]:
        return self._fields.get(name)

    @staticmethod
    def __get_fields_file_path() -> str:
        return os.path.join(os.path.dirname(__file__), '../data/fields.json')
