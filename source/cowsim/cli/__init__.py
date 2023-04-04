import click


@click.group()
@click.version_option()
def root():
    """A simple cow pen simulator."""
    pass


def main():
    root()
