from dataclasses import dataclass, field

from src.domain.entities.base_lxml import BaseLxmlEntity


@dataclass(eq=False)
class InMemoryDatabase:
    _storage: list[BaseLxmlEntity] = field(default_factory=list)

    def add_entity(self, entity: BaseLxmlEntity):
        self._storage.append(entity)

    def check_entity_exists(self, entity: BaseLxmlEntity):

        try:
            return next(product for product in self._storage if product == entity)
        except StopIteration:
            return False
