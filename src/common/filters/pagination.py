from dataclasses import dataclass


@dataclass(eq=False)
class PaginationFilters:
    offset: int = 0
    limit: int = 10
