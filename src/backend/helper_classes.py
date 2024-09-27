from dataclasses import dataclass
from typing import Optional
from configuration import logger

LatLong = tuple[Optional[float], Optional[float]]


@dataclass
class Address:
    source: str
    source_id: str
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

    def __init__(self, input_row, col_map):
        for field, idx in col_map.items():
            setattr(self, field, input_row[idx])
        self.lat_long = (self.lattitude, self.longitude)
