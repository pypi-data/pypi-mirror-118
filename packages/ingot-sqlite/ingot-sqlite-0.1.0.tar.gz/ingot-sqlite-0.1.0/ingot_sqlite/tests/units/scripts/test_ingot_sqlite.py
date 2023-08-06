import typing as t

from ingots.tests.units.scripts import test_base

from ingot_sqlite.scripts.ingot_sqlite import IngotSqliteDispatcher

__all__ = ("IngotSqliteDispatcherTestCase",)


class IngotSqliteDispatcherTestCase(test_base.BaseDispatcherTestCase):
    """Contains tests for the IngotSqliteDispatcher class and checks it."""

    tst_cls: t.Type = IngotSqliteDispatcher
    tst_builder_name = "test"
