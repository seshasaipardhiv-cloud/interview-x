"""Load and query organizer-provided curriculum data."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from app.models.curriculum import Curriculum, CurriculumDay, CurriculumModule

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "curriculum.json"


class CurriculumService:
    """Read-only access to curriculum.json."""

    def __init__(self, data_path: Path | None = None) -> None:
        self._data_path = data_path or DATA_PATH
        self._curriculum: Curriculum | None = None
        self._days_by_number: dict[int, CurriculumDay] = {}
        self._modules_by_number: dict[int, CurriculumModule] = {}
        self._module_for_day: dict[int, int] = {}

    def load_curriculum(self) -> Curriculum:
        """Load and cache curriculum.json."""
        if self._curriculum is None:
            with self._data_path.open(encoding="utf-8") as handle:
                payload = json.load(handle)
            self._curriculum = Curriculum.model_validate(payload)
            self._index_curriculum()
        return self._curriculum

    def _index_curriculum(self) -> None:
        assert self._curriculum is not None
        self._days_by_number = {day.day: day for day in self._curriculum.days}
        self._modules_by_number = {module.n: module for module in self._curriculum.modules}
        self._module_for_day = {}
        for module in self._curriculum.modules:
            if len(module.days) >= 2:
                start_day, end_day = module.days[0], module.days[-1]
                for day_number in range(start_day, end_day + 1):
                    self._module_for_day[day_number] = module.n
            else:
                for day_number in module.days:
                    self._module_for_day[day_number] = module.n

    def get_all_modules(self) -> list[CurriculumModule]:
        """Return all curriculum modules."""
        return self.load_curriculum().modules

    def get_all_days(self) -> list[CurriculumDay]:
        """Return all curriculum days in ascending order."""
        days = self.load_curriculum().days
        return sorted(days, key=lambda item: item.day)

    def get_day(self, day_number: int) -> CurriculumDay | None:
        """Return a single curriculum day by number."""
        self.load_curriculum()
        return self._days_by_number.get(day_number)

    def get_module(self, module_number: int) -> CurriculumModule | None:
        """Return a single module by module number."""
        self.load_curriculum()
        return self._modules_by_number.get(module_number)

    def get_topic_days(self) -> dict[int, CurriculumDay]:
        """Return day-number → curriculum day mapping (topic index)."""
        self.load_curriculum()
        return dict(self._days_by_number)

    def get_related_days(self, day_number: int) -> list[CurriculumDay]:
        """Return other days in the same module as the given day."""
        self.load_curriculum()
        module_number = self._module_for_day.get(day_number)
        if module_number is None:
            return []
        module = self._modules_by_number[module_number]
        if len(module.days) >= 2:
            start_day, end_day = module.days[0], module.days[-1]
            related_numbers = [
                day for day in range(start_day, end_day + 1) if day != day_number
            ]
        else:
            related_numbers = [day for day in module.days if day != day_number]
        return [
            self._days_by_number[number]
            for number in sorted(related_numbers)
            if number in self._days_by_number
        ]

    def get_module_for_day(self, day_number: int) -> CurriculumModule | None:
        """Return the module containing a curriculum day."""
        self.load_curriculum()
        module_number = self._module_for_day.get(day_number)
        if module_number is None:
            return None
        return self._modules_by_number.get(module_number)


@lru_cache(maxsize=1)
def get_curriculum_service() -> CurriculumService:
    """Shared curriculum service instance."""
    service = CurriculumService()
    service.load_curriculum()
    return service
