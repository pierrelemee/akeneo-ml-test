from typing import Optional

from src.models import ProductField
from abc import ABC, abstractmethod


class ProductFieldManager(ABC):
    """
    Abstract service class capable of fetching data about a known field.
    """

    @abstractmethod
    def get_field(self, name: str) -> Optional[ProductField]:
        pass


class DatabaseProductFieldManager(ProductFieldManager):
    def get_field(self, name: str) -> Optional[ProductField]:
        return ProductField.get_or_none(ProductField.name == name)
