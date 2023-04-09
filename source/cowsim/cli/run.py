import click
from cowsim import engine
from cowsim.entity.cow.purple_angus import PurpleAngus
from cowsim.environment.cowpen import CowPen

ENVIRONMENT_CHOICES = [CowPen.name()]
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
@click.option(
    "-o",
    "--output-dir",
    "output_dir",
    type=click.Path(exists=False),
    default="./data",
    help="Output directory for simulation data.",
)
@click.option(
    "-c",
    "--capacity",
    "capacity",
    type=click.INT,
    default=100,
    help="Set the max capacity of the environment.",
)
@click.option(
    "-s",
    "--steps",
    "steps",
    type=click.INT,
    default=365,
    help="Set the number of simulation steps to run.",
)
def run(environment, entities, output_dir, capacity, steps):
    """Run a cow pen simulation."""
    engine.run(
        environment=environment,
        entities=entities,
        output_dir=output_dir,
        capacity=capacity,
        steps=steps,
    )
