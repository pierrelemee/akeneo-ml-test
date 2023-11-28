import json
import os

import typer

from src.models import ProductField, ProductFieldValue, db

app = typer.Typer()


@app.command()
def load_data():
    # Load field database from json file
    field_names = []
    with open(os.path.join(os.path.dirname(__file__), "./data/fields.json")) as file:
        fields = json.loads(file.read())
        ProductField.truncate_table(restart_identity=True, cascade=True)

        for field in fields:
            ProductField.create(
                name=field["name"],
                label=field["label"],
                type=field["type"],
                multiple=field["multiple"],
                options=", ".join(field["options"])
                if "options" in fields
                else None,  # Doesn't work
            )

    with open(os.path.join(os.path.dirname(__file__), "./data/examples.json")) as file:
        examples = json.loads(file.read())
        ProductFieldValue.truncate_table(restart_identity=True, cascade=True)

        for example in examples:
            if (
                example["field_value"] is not None
                and example["LIBL_LIBELLE"] is not None
                and example["Argumentaire Produit"] is not None
                and ProductField.get(name=example["field_name"]) is not None
            ):
                ProductFieldValue.create(
                    name=example["field_name"],
                    value=example["field_value"],
                    context=example["LIBL_LIBELLE"]
                    if example["LIBL_LIBELLE"] is not None
                    else example["Argumentaire Produit"],
                )


if __name__ == "__main__":
    app()
