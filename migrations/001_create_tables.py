"""Peewee migrations -- 001_create_tables.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class ProductField(pw.Model):
        name = pw.CharField(max_length=255, primary_key=True)
        label = pw.CharField(max_length=255)
        type = pw.CharField(max_length=255)
        multiple = pw.BooleanField(default=False)
        options = pw.TextField(null=True)

        class Meta:
            table_name = "fields"

    @migrator.create_model
    class ProductFieldValue(pw.Model):
        id = pw.AutoField()
        name = pw.ForeignKeyField(column_name='name_id', field='name', model=migrator.orm['fields'])
        context = pw.TextField()
        value = pw.CharField(max_length=255, null=True)

        class Meta:
            table_name = "field_values"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('field_values')

    migrator.remove_model('fields')
