#!/usr/bin/env python
import click
import json

from janus.app import Janus


@click.command()
@click.option('-f', '--file', required=True, help='source code file')
def main(file):
    """
    Args:
        file (str): the path of a file
    """
    engine = Janus()
    res = engine.process(file)
    click.echo(json.dumps(res))


if __name__ == '__main__':
    main()
