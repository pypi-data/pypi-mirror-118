from logging import getLogger

from ingots.bootstrap.base import BaseBuilder

import ingot_psql as package

__all__ = ("IngotPsqlBaseBuilder",)


logger = getLogger(__name__)


class IngotPsqlBaseBuilder(BaseBuilder):

    package = package
