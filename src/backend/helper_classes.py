from dataclasses import dataclass
from typing import Optional
from src.configuration import logger

from thefuzz import (
    ratio,
    partial_ratio,
    token_sort_ratio,
    token_set_ratio,
    partial_token_sort_ratio,
    partial_token_set_ratio,
)

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

    full_address: Optional[str] = None

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
        
        if  self.address_two:
            full_address = self.address_one + ' ' + self.address_two
        else:
            full_address = self.address_one
        self.full_address = full_address
        


@dataclass
class MatchTuple:
    '''A tuple of matched addresses, 
        intended to summarize the strength of a match.
        Assists in the match ranking process'''
    search_address: object
    matched_address: object
    cols_matched: list[tuple[str, str]]
    match_strength: dict = None

    fuzz_stats: dict = None
    avg_match_score: int = None
    avg_fuzz_score: int = None
    
    def __post_init__(self):
        search_address_str = self.full_address
        matched_address_str = self.full_address
        match_functions:list[callable] =  [ratio,
                            partial_ratio,
                            token_sort_ratio,
                            token_set_ratio,
                            partial_token_sort_ratio,
                            partial_token_set_ratio,]
        self.fuzz_stats = { func.__name__: 
                                    func(search_address_str, 
                                         matched_address_str) 
                                for func in match_functions}

    def __getitem__(self, attr: str) -> Any:
        return getattr(self, attr)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MatchTuple):
            return False
        return self.compare(self, other) in ('same', 'eq')

    def differs(self, other, field) -> str:
         """Similar to a __sub__ func
             Supports the compare method""" 
         if self[field] > other[field]:
              return 'gt'
         if self[field]< other[field]:
              return 'lt'
         else:
              return None
    
    def compare(self, other):
         """ Compares two matches 
         """
         same_addr = self.search_address_id == other.search_address_id
         if same_addr:
              return 'same'
         else:
              for field in ['match_str', 'avg_match_score', 'avg_fuzz_score']:
                   decision = self.differs(other, field)
                   if decision:
                        return decision
                   else:
                        return 'eq'