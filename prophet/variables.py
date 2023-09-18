import struct
from typing import List
from typing import Set
from typing import Union
import pandas as pd
import regex as re
from prophet.config import valid_var_regex
from prophet.indicators import ProductIndicators


class ProductVariables(ProductIndicators):

    def __init__(self, dsn: str, prod_name: str):
        super().__init__(dsn=dsn, prod_name=prod_name)
        self.lib_name: str = self.prod_to_lib_name.get(prod_name)
        self.vars: pd.DataFrame = self.get_vars()
        self.var_names: Set[str] = set(self.vars['var_name'].unique())
        self.set_var_deps()

    def get_vars(self) -> pd.DataFrame:

        def get_core_vars():
            core_vars = self.variables.copy()
            core_vars.query(f'lib_name == "{self.lib_name}" & input_var_flag == 0', inplace=True)
            core_vars['ind_expr_val'] = core_vars['ind_expr'].map(self.get_expr_val)
            core_vars.query('ind_expr_val == True', inplace=True)
            core_vars.drop(columns=['ind_expr_val'], inplace=True)
            return core_vars

        def get_input_vars():
            input_vars = self.variables.copy()
            input_vars.query(f'prod_name == "{self.prod_name}" & input_var_flag == 1', inplace=True)
            return input_vars

        return pd.concat([get_core_vars(), get_input_vars()], ignore_index=True).sort_values(by=['var_name'])

    def set_var_deps(self) -> None:

        def decode_formula(var_expr: bytes) -> Union[str, float]:
            formula_defn = var_expr
            try:
                formula_defn = struct.unpack('d', var_expr)[0]
            except struct.error:
                formula_defn = var_expr[:-1].decode(encoding='utf-8')
            finally:
                return formula_defn

        def depends_on(formula: str) -> List[str]:
            if isinstance(formula, str):
                return sorted(filter(None, [
                    var_name if var_name in self.var_names else None
                    for var_name in set(re.findall(valid_var_regex, formula))
                ]))
            else:
                return []

        df = self.vars
        df['var_expr'] = df['var_expr'].apply(decode_formula)
        df['depends_on'] = df['var_expr'].apply(depends_on)
