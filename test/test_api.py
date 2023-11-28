import os
from typing import List

import pytest

from fastapi.testclient import TestClient

from src.models import ProductField


class TestAPI:
    """
    Test http calls to the FastAPI app.
    """

    @pytest.fixture
    def input_fields(self):
        ProductField.get_or_create(
            name="EF001438", multiple=False, label="longueur (cm)", type="number"
        )

        return ["EF001438", "EF999999"]

    def test_lookup_product_fields_success(self, input_fields: List[str]):
        """
        Test POST http calls to the `/api/product/fields/lookup`, expecting successful output
        :return:
        """
        os.environ["CONFIG_MODULE"] = "config.example"

        from web import app

        client = TestClient(app)

        response = client.post(
            "/api/product/fields/lookup",
            json={
                "description": "Baignoire d'angle Geberit Bastia: 142x142cm",
                "llm": "llama2",
                "fields": input_fields,
            },
        )
        assert response.status_code == 200
        res = response.json()

        # Known product should be matched
        assert res["EF001438"] == "Answer LLaMA"
        # Unknown product should remain unmatched
        assert res["EF999999"] is None
