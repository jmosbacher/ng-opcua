# -*- coding: utf-8 -*-

"""Console script for ng_opcserver."""
import sys
import click
import ng_opcserver


@click.command()
@click.option("--duration", default=10, help="Serve duration.")
@click.option("--frequency", default=1, help="Change frequency.")
@click.option("--debug", is_flag=True, default=False, help="Debug.")
def main(duration, frequency, debug):
    ng_opcserver.run_server(duration, frequency, debug)
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
