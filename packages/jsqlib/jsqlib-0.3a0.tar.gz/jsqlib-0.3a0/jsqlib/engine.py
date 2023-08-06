""" This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at https://mozilla.org/MPL/2.0/.

Created on Jul 29, 2021

@author: pymancer@gmail.com (polyanalitika.ru)
"""
import json
import sqlfluff

from typing import Optional, List, Dict, Type
from sqlfluff.core.dialects import dialect_selector
from jinja2 import Template
from jsqlib.core import Builder, DIALECTS
from jsqlib.helpers.constants import POSTGRESQL_DIALECT, QUERY_KEY
from jsqlib.helpers.types import SD_T, SIBN_T


class Query:
    """JSON to SQL query generator."""

    def __init__(
        self,
        raw: Optional[SD_T] = None,
        dialect: str = POSTGRESQL_DIALECT,
        constants: Optional[Dict[str, SIBN_T]] = None,
        bindings: Optional[Dict[str, SIBN_T]] = None,
        builder_cls: Optional[Type[Builder]] = None,
        **kwargs,
    ) -> None:

        self._raw = raw
        self._dialect = dialect
        self._bindings = bindings or dict()
        self._body = None
        self._sql = None

        if builder_cls:
            self.builder = builder_cls(constants=constants, **kwargs)
        else:
            self.builder = self._get_builder(self._dialect, constants=constants, **kwargs)

    @property
    def sql(self) -> str:
        if self._sql is None:
            self._sql = self._build()

        return self._sql

    @property
    def body(self) -> dict:
        if self._body is None:
            if isinstance(self._raw, str):
                raw = json.loads(Template(self._raw).render(self._bindings))
            else:
                raw = self._raw or dict()

            self._body = raw.get(QUERY_KEY, raw)

        return self._body

    def prettify(
        self, sql: Optional[str] = None, dialect: Optional[str] = None, rules: Optional[List[str]] = None
    ) -> str:

        sql = sql or self.sql
        dialect = dialect or self._dialect

        if dialect == POSTGRESQL_DIALECT:
            dialect = 'postgres'

        try:
            dialect_selector(dialect)
        except KeyError:
            dialect = 'ansi'

        return sqlfluff.fix(sql, dialect=dialect, rules=rules) if sql else sql

    def _build(self, *args, **kwargs) -> str:
        built = ''

        if self.body is not None:
            built = self.builder.build(self.body)

        return built

    def _get_builder(self, dialect: str, **kwargs) -> Builder:
        return DIALECTS[dialect](**kwargs)
