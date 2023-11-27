import os
from concurrent.futures import ThreadPoolExecutor, wait
from time import time
from typing import Annotated, Callable, Dict

from fastapi import Depends

from src.models.llms import AbstractLLM
from src.models.product import Field
from src.models.query import ProductFieldsLookupQuery
from src.services.field import FieldManager, JsonFileFieldManager


class ProductLookupManager:
    _field_manager: FieldManager

    def __init__(
        self, field_manager: Annotated[FieldManager, Depends(JsonFileFieldManager)]
    ):
        super().__init__()
        self._field_manager = field_manager
        self._timeout = int(os.getenv("LLM_QUERY_TIMEOUT", "20"))

    def lookup_product_fields(
        self, query: ProductFieldsLookupQuery, get_llm: Callable[[], AbstractLLM]
    ) -> Dict:
        fields = {name: self._field_manager.get_field(name) for name in query.fields}
        # Initialize the values result dict with None
        values = {name: None for name in fields.keys()}

        with ThreadPoolExecutor() as executor:
            start = time()
            # Run lookup task, for a single product field, in parallel with a timeout
            futures = [
                executor.submit(
                    self.lookup_product_field, query.description, field, get_llm
                )
                for field in fields.values()
                if field is not None
            ]

            # wait for all tasks to complete
            completed, _ = wait(futures, timeout=self._timeout)
            stop = time()
            # report the number of tasks done
            print(f"Tasks done: {len(completed)} in {stop - start}s")

            for future in completed:
                name, value = future.result()
                values[name] = value

            # Cf. doc "It is safe to call this method several times. Otherwise, no other methods can be called after
            # this one"
            executor.shutdown(wait=False, cancel_futures=True)
            executor.shutdown(wait=False, cancel_futures=True)
            executor.shutdown(wait=False, cancel_futures=True)

        return values

    def lookup_product_field(
        self,
        description: str,
        field: Field,
        get_llm: Callable[[], AbstractLLM],
    ):
        llm: AbstractLLM = get_llm()
        return (
            field.name,
            llm.lookup_field_description(field, description)
            if isinstance(llm, AbstractLLM)
            else None,
        )
