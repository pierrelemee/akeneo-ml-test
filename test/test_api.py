from fastapi import FastAPI
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


class TestAPI:
    """
    Test http calls to the FastAPI app.
    """

    def test_lookup_product_fields_success(self):
        """
        Test POST http calls to the `/api/product/fields/lookup`, expecting successful output
        :return:
        """
        response = client.post(
            "/api/product/fields/lookup",
            json={
                "description": "Baignoire d'angle Geberit Bastia: 142x142cm",
                "llm": "llama2",
                "fields": ["EF001438", "EF999999"],
            },
        )
        assert response.status_code == 200
        res = response.json()

        # Known product should be matched
        assert res["EF001438"] == "longueur (cm)"
        # Unknown product should remain unmatched
        assert res["EF999999"] is None