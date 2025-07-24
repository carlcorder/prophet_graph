from functools import cache
from typing import Dict
import pandas as pd
import regex as re
from sympy.parsing.sympy_parser import parse_expr
from prophet.workspace import ProphetWorkspace as PrW


class ProductIndicators(PrW):

    def __init__(self, dsn: str, prod_name: str):
        super().__init__(dsn=dsn)
        self.prod_name: str = prod_name
        self.schedule: pd.DataFrame = self.get_schedule()

    def get_schedule(self) -> pd.DataFrame:
        return (
            # TODO: Check secondary input variables are properly handled
            self.indicators.query('prod_name.notnull()')
            .filter(items=['prod_name', 'ind_name', 'ind_id'], axis='columns')
            .pivot(index='ind_name', columns='prod_name', values='ind_id').notna()
        )

    @cache
    def get_prod_schedule(self, prod_name: str = '') -> Dict[str, bool]:
        return self.schedule[prod_name].to_dict()

    @cache
    def get_expr_val(self, ind_expr: str = '') -> bool:

        reserved = [*['AND', 'OR', 'NOT'], *['(', ')', '[', ']', '{', '}']]  # Operators and Separators
        parens = re.compile('([]()[{}])|\\s')

        def normalize(expr: str) -> str:
            return expr.replace('[', '(').replace(']', ')').replace('{', '(').replace('}', ')')

        def get_tokenized_expr() -> str:
            tokenized_expr = str(False)
            if tokens := list(filter(None, re.split(parens, normalize(ind_expr)))):
                prod_schedule = self.get_prod_schedule(prod_name=self.prod_name)
                tokenized_expr = (
                    ' '.join([token if token in reserved else str(prod_schedule.get(token, False)) for token in tokens])
                )
            return tokenized_expr.lower()

        return bool(parse_expr(get_tokenized_expr()))
