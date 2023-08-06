from logging import getLogger

from ingots.bootstrap.base import BaseBuilder

import ingot_sqlite as package

__all__ = ("IngotSqliteBaseBuilder",)


logger = getLogger(__name__)


class IngotSqliteBaseBuilder(BaseBuilder):

    package = package
