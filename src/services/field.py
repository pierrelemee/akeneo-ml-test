from typing import List, Dict, Optional
import os

from pydantic import TypeAdapter

from src.models.product import Field
from abc import ABC, abstractmethod


class FieldManager(ABC):
    """
    Abstract service class capable of fetching data about a known field.
    """

    @abstractmethod
    def get_field(self, name: str) -> Optional[Field]:
        pass


class JsonFileFieldManager(FieldManager):
    """
    Implementation of FieldManager reading data from a static JSON file.
    """

    # In memory database
    _fields: Dict[str, Field] = None

    def _load_database(self):
        # If database hasn't been initialized yet
        if self._fields is None:
            # Load field database from json file
            with open(self.__get_fields_file_path()) as file:
                self._fields = {
                    field.name: field
                    for field in TypeAdapter(List[Field]).validate_json(file.read())
                }

    def get_field(self, name: str) -> Optional[Field]:
        self._load_database()

        return self._fields.get(name)

    @staticmethod
    def __get_fields_file_path() -> str:
        return os.path.join(os.path.dirname(__file__), "../../data/fields.json")
