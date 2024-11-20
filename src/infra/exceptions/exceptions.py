from dataclasses import dataclass
from typing import Any

from sqlalchemy.exc import SQLAlchemyError


@dataclass(eq=False)
class SQLException(SQLAlchemyError):
    data: Any

    @property
    def message(self):
        return f"SQLAlchemy error occurred {self.data=}"
