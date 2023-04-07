import click
from .run import run


@click.group()
@click.version_option()
def root():
    """A simple cow pen simulator."""
    pass


def main():
    root.add_command(run)
    root()
