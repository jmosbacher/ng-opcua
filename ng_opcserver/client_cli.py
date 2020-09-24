# -*- coding: utf-8 -*-

"""Console script for ng_opcserver."""
import sys
import click
import ng_client


@click.command()
@click.option("--duration", default=10, help="Poll duration.")
@click.option("--frequency", default=1, help="Poll frequency.")
@click.option("--debug", is_flag=True, default=False, help="Debug.")
def main(duration, frequency, debug):
    ng_client.run_poll_status(duration, frequency, debug)
    return 0

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
