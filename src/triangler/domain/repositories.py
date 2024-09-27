from typing import Generic
from typing import Self
from typing import TypeVar

from sqlalchemy import ColumnElement
from sqlalchemy import select
from sqlalchemy.orm import Session

from triangler.data import models
from triangler.domain import schemas

SchemaIn = TypeVar("SchemaIn", bound=schemas.TrianglerBaseInSchema)
SchemaOut = TypeVar("SchemaOut", bound=schemas.TrianglerBaseOutSchema)
DataModel = TypeVar("DataModel", bound=models.TrianglerBaseModel)


class Repository(Generic[DataModel, SchemaIn, SchemaOut]):
    def __init__(
        self: Self,
        session: Session,
        data_model: type[DataModel],
        schema_in: type[SchemaIn],
        schema_out: type[SchemaOut],
    ) -> None:
        self.session = session
        self.data_model = data_model
        self.schema_in = schema_in
        self.schema_out = schema_out

    def get_all(self: Self) -> list[SchemaOut]:
        results = [
            self.schema_out.model_validate(x)
            for x in self.session.scalars(select(self.data_model))
        ]
        return results

    def get_by_id(self: Self, id: int) -> SchemaOut:
        result = self.session.get_one(self.data_model, id)
        result_schema = self.schema_out.model_validate(result)
        return result_schema

    def filter(self: Self, *filters: ColumnElement[bool]) -> list[SchemaOut]:
        results = [
            self.schema_out.model_validate(x)
            for x in self.session.scalars(select(self.data_model).filter(*filters))
        ]
        return results

    def create(self: Self, data: SchemaIn) -> SchemaOut:
        with self.session.begin():
            new_data = self.data_model(**data.model_dump())
            self.session.add(new_data)
            self.session.commit()
        result_schema = self.schema_out.model_validate(new_data)
        return result_schema

    def update(self: Self, data: SchemaOut) -> SchemaOut:
        with self.session.begin():
            result = self.session.get_one(self.data_model, data.id)
            for key, value in data.model_dump().items():  # pyright: ignore[reportAny]
                setattr(result, key, value)
            self.session.add(result)
            self.session.commit()
        result_schema = self.schema_out.model_validate(result)
        return result_schema

    def delete(self: Self, id: int) -> None:
        with self.session.begin():
            result = self.session.get_one(self.data_model, id)
            self.session.delete(result)


ExperimentRepository = Repository[
    models.Experiment, schemas.ExperimentInSchema, schemas.ExperimentOutSchema
]

SampleFlightRepository = Repository[
    models.SampleFlight, schemas.SampleFlightInSchema, schemas.SampleFlightOutSchema
]

ObservationRepository = Repository[
    models.Observation, schemas.ObservationInSchema, schemas.ObservationOutSchema
]

SampleFlightTokenRepository = Repository[
    models.SampleFlightToken,
    schemas.SampleFlightTokenInSchema,
    schemas.SampleFlightTokenOutSchema,
]
