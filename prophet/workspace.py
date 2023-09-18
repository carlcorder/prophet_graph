from functools import cached_property
from typing import Dict
import fdb
import pandas as pd
from prophet.config import var_type, defn_type


class ProphetWorkspace:

    def __init__(self, dsn: str):
        self.conn: fdb.Connection = fdb.connect(dsn=dsn, user='sysdba', password='masterkey')
        self.products: pd.DataFrame = self.get_products()
        self.variables: pd.DataFrame = self.get_variables()
        self.indicators: pd.DataFrame = self.get_indicators()

    @staticmethod
    def fetch(conn: fdb.Connection, name: str = '') -> pd.DataFrame:
        with open(f"./sql/{name}", 'r') as file:
            return pd.read_sql_query(file.read(), conn)

    def get_products(self) -> pd.DataFrame:
        return self.fetch(self.conn, name='products.sql')

    def get_variables(self) -> pd.DataFrame:
        return self.fetch(self.conn, name='variables.sql').replace({'var_type': var_type, 'defn_type': defn_type})

    def get_indicators(self) -> pd.DataFrame:
        return self.fetch(self.conn, name='indicators.sql')

    @cached_property
    def prod_to_lib_name(self) -> Dict:
        return dict(zip(self.products['prod_name'], self.products['lib_name']))
