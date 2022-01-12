#!/usr/bin/env python
import click
import json

from janus.app import Janus


@click.command()
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def main(paths):
    """
    Args:
        paths (tuple): the paths of files or directories
    """
    engine = Janus()
    res = engine.process(paths)
    click.echo(json.dumps(res))


if __name__ == '__main__':
    main()
