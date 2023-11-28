from typing import Optional

import os

from urllib.parse import urlparse
from peewee import (
    PostgresqlDatabase,
    Model,
    CharField,
    BooleanField,
    AutoField,
    ForeignKeyField,
    TextField,
)

# Hack to convert a JDBC-like URL to a valid Peewee connection
db_url = urlparse(os.getenv("DATABASE_URL"))
db = PostgresqlDatabase(
    db_url.path.replace("/", ""),
    user=db_url.username,
    password=db_url.password,
    host=db_url.hostname,
    port=db_url.port,
)
"""
Generating a migration:

```bash
pw_migrate create --auto --auto-source src.models --database $DATABASE_URL <name>
```

Run a migration:

```bash
pw_migrate  migrate --database $DATABASE_URL
```

"""


class ProductField(Model):
    class Meta:
        table_name = "fields"
        database = db

    name: str = CharField(default=None, primary_key=True, index=True)
    label: str = CharField(null=False)
    type: str = CharField(null=False)
    multiple: bool = BooleanField(null=False, default=False)
    options: Optional[str] = TextField(default=None, null=True)


class ProductFieldValue(Model):
    class Meta:
        table_name = "field_values"
        database = db

    id = AutoField()
    name: str = ForeignKeyField(ProductField, backref="values", lazy_load=False)
    context: str = TextField()
    value: str = CharField(null=True)
