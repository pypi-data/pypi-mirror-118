import typing as t

from ingots.tests.units.bootstrap import test_base

from ingot_sqlite.bootstrap import IngotSqliteBaseBuilder

__all__ = ("IngotSqliteBaseBuilderTestCase",)


class IngotSqliteBaseBuilderTestCase(test_base.BaseBuilderTestCase):
    """Contains tests for the IngotSqliteBuilder class."""

    tst_cls: t.Type = IngotSqliteBaseBuilder
    tst_entity_name: str = "ingot_sqlite"
    tst_entity_name_upper: str = "INGOT_SQLITE"
    tst_entity_name_class_name: str = "IngotSqlite"
    tst_entity_description = (
        "Provides integration with the SQLite DB for Ingots projects"
    )
