from dataclasses import dataclass
from typing import Optional
from src.configuration import logger

from thefuzz.fuzz import (
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
    
    def __lt__(self, value: object) -> bool:
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
    match_strength: dict = None

    fuzz_stats: dict = None
    avg_fuzz_score: int = None
    
    def __init__(self,search_address, matched_address):
        self.search_address = search_address
        self.matched_address = matched_address
        search_address_str =  search_address.full_address
        matched_address_str = matched_address.full_address
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
        scores = self.fuzz_stats.values()
        self.avg_fuzz_score = sum(scores)/len(scores)

    def __getitem__(self, attr: str):   
        return getattr(self, attr)
    
    def get(self, attr: str, default=None):   
        try:
            return getattr(self, attr)
        except AttributeError:
            return default

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MatchTuple):
            return False
        return self.compare(other) in ('same', 'eq')

    def differs(self, other, field) -> str:
        """Similar to a __sub__ func
            Supports the compare method"""
        if self.get(field) and other.get(field):
            if self[field] > other[field]:
                return 'gt'
            if self[field]< other[field]:
                return 'lt'
            if self[field] == other[field]:
                return 'eq'
        return None
    
    def compare(self, other):
         """ Compares two matches 
         """
         same_addr = self.search_address == other.search_address
         if same_addr:
              return 'same'
         else:
              for field in ['match_strength', 'avg_fuzz_score']:
                   decision = self.differs(other, field)
                   if decision:
                        return decision
                   else:
                        return 'eq'