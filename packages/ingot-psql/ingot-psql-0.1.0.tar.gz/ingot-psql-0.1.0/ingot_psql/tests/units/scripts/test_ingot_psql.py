import typing as t

from ingots.tests.units.scripts import test_base

from ingot_psql.scripts.ingot_psql import IngotPsqlDispatcher

__all__ = ("IngotPsqlDispatcherTestCase",)


class IngotPsqlDispatcherTestCase(test_base.BaseDispatcherTestCase):
    """Contains tests for the IngotPsqlDispatcher class and checks it."""

    tst_cls: t.Type = IngotPsqlDispatcher
    tst_builder_name = "test"
