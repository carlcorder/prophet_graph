import json
from prophet.variables import ProductVariables


class ProphetGraph(ProductVariables):

    def __init__(self, dsn: str, prod_name: str):
        super().__init__(dsn=dsn, prod_name=prod_name)
        self.json: str = json.dumps(dict(zip(self.vars['var_name'], self.vars['depends_on'])))

# TODO: Json needs to match format expected by MSAGL.js (https://microsoft.github.io/msagljs/)
