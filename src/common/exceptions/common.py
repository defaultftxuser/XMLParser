from dataclasses import dataclass
from typing import Any


@dataclass(eq=False)
class CommonException(BaseException):
    data: Any

    @property
    def message(self):
        return f"Error occurred {self.data}"
