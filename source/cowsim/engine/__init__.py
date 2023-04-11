from cowsim.environment.cowpen import CowPen
from cowsim.entity.cow.purple_angus import PurpleAngus

DEFAULT_PURPLE_ANGUS_POPULATION = 10

ENVIRONMENT_MAP = {
    CowPen.name: CowPen,
}

ENTITY_MAP = {
    PurpleAngus.name: PurpleAngus,
}


def run(
    environment: str,
    entities: ((str, int)),
    output_dir: str,
    capacity: int,
    steps: int,
) -> None:
    if environment is None:
        environment = CowPen.name

    entity_list = []
    for entity in entities:
        entity_list.append(entity)
    entities = entity_list

    if len(entities) == 0:
        entities.append((PurpleAngus.name, DEFAULT_PURPLE_ANGUS_POPULATION))

    env_cls = ENVIRONMENT_MAP[environment]
    entities = [(ENTITY_MAP[entity[0]], entity[1]) for entity in entities]

    env_instance = env_cls(
        entities=entities,
        max_capacity=capacity,
        max_steps=steps,
    )
    env_instance.run()
    env_instance.report(output_dir)
