from dataclasses import dataclass
from typing import Optional
from src.configuration import logger

LatLong = tuple[Optional[float], Optional[float]]


@dataclass
class Address:
    source: Optional[str] = None
    source_id: Optional[str] = None
    name: Optional[str] = None
    address_one: Optional[str] = None
    address_two: Optional[str] = None
    locality: Optional[str] = None
    state: Optional[str] = None
    state_code: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    country_code: Optional[str] = None
    lattitude: Optional[float] = None
    longitude: Optional[float] = None

    lat_long: LatLong = None
    # state_level_category None

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Address):
            return False
        return all(
            getattr(self, field) == getattr(value, field)
            for field in self.__dataclass_fields__.keys()
        )

    def from_data(self, input_row, col_map):
        for field, idx in col_map.items():
            setattr(self, field, input_row[idx])
        self.lat_long = (self.lattitude, self.longitude)
