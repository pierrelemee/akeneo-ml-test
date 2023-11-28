from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from src.models import ProductField
from abc import ABC, abstractmethod

from src.database import get_db, engine


class ProductFieldManager(ABC):
    """
    Abstract service class capable of fetching data about a known field.
    """

    @abstractmethod
    def get_field(self, name: str) -> Optional[ProductField]:
        pass


class DatabaseProductFieldManager(ProductFieldManager):
    _session: Session

    def __init__(self, session: Session = Depends(get_db)):
        super().__init__()

        self._session = session

    def get_field(self, name: str) -> Optional[ProductField]:
        return self._session.get(ProductField, name)


ProductField.metadata.create_all(bind=engine)
