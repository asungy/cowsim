import click
from cowsim import engine
from cowsim.entity.cow.purple_angus import PurpleAngus

ENVIRONMENT_CHOICES = ["cowpen"]
ENTITY_CHOICES = [PurpleAngus.name()]


@click.command()
@click.option(
    "-e",
    "--environment",
    type=click.Choice(ENVIRONMENT_CHOICES, case_sensitive=False),
    default=None,
    help="Set the simulation environment.",
)
@click.option(
    "-t",
    "--entity",
    "entities",
    type=(str, int),
    default=None,
    multiple=True,
    help=f"Set entities and quantity to run in simulation. Options: {ENTITY_CHOICES}",
)
def run(environment, entities):
    """Run a cow pen simulation."""
    engine.run(environment, entities)
