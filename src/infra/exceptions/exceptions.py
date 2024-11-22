from dataclasses import dataclass
from typing import Any

from pymongo.errors import WriteError, OperationFailure
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


@dataclass(eq=False)
class SQLException(SQLAlchemyError):
    data: Any

    @property
    def message(self):
        return f"SQLAlchemy error occurred {self.data=}"


@dataclass(eq=False)
class SQLIntegrityError(IntegrityError):
    data: Any

    @property
    def message(self):
        return f"Product must be unique and must appear in one category"


@dataclass(eq=False)
class MongoWriteError(WriteError):

    @property
    def message(self):
        return f"Mongo db error during write"


@dataclass(eq=False)
class MongoOperationError(OperationFailure):

    @property
    def message(self):
        return f"Mongo db error occurred"
