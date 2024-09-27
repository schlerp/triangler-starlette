from triangler.domain.repositories import ExperimentRepository
from triangler.domain import schemas


def get_all_experiments(
    *, repository: ExperimentRepository
) -> list[schemas.ExperimentOutSchema]:
    """Gets all experiemnts from the database."""
    results = repository.get_all()
    return results


def get_experiment_by_id(
    *, id: int, repository: ExperimentRepository
) -> schemas.ExperimentOutSchema | None:
    """Gets an experiment by its id."""
    result_schema = repository.get_by_id(id)
    return result_schema


def create_experiment(
    *, experiement_data: schemas.ExperimentInSchema, repository: ExperimentRepository
) -> schemas.ExperimentOutSchema:
    """Creates a new experiment."""
    result_schema = repository.create(experiement_data)
    return result_schema


def update_experiment(
    *, experiment_data: schemas.ExperimentOutSchema, repository: ExperimentRepository
) -> schemas.ExperimentOutSchema:
    """Updates an experiment."""
    result_schema = repository.update(experiment_data)
    return result_schema


def delete_experiment(*, experiment_id: int, repository: ExperimentRepository) -> None:
    """Deletes an experiment by its id."""
    repository.delete(experiment_id)
