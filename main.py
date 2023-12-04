import argparse
import config
from prophet.graph import ProphetGraph

parser = argparse.ArgumentParser(description="Prophet Graph Generator")
parser.add_argument("--dsn", help="Connection string in format [host[/port]]:database")
parser.add_argument("--prod_name", help="Master product name")
cli_args = parser.parse_args()


def main(dsn: str, prod_name: str) -> None:
    graph = ProphetGraph(dsn=dsn, prod_name=prod_name)
    print(graph.json)


if __name__ == '__main__':
    main(**vars(cli_args))  # main(dsn=config.dsn, prod_name=config.prod_name)
