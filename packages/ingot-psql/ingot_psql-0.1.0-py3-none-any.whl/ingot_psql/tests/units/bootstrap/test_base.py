import typing as t

from ingots.tests.units.bootstrap import test_base

from ingot_psql.bootstrap import IngotPsqlBaseBuilder

__all__ = ("IngotPsqlBaseBuilderTestCase",)


class IngotPsqlBaseBuilderTestCase(test_base.BaseBuilderTestCase):
    """Contains tests for the IngotPsqlBuilder class."""

    tst_cls: t.Type = IngotPsqlBaseBuilder
    tst_entity_name: str = "ingot_psql"
    tst_entity_name_upper: str = "INGOT_PSQL"
    tst_entity_name_class_name: str = "IngotPsql"
    tst_entity_description = (
        "Provides integration with the PostgresQL DB for Ingots projects"
    )
