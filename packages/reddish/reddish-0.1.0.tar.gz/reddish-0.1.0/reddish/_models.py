from dataclasses import dataclass
from typing import Counter

class Ok:
    
    @classmethod
    def __get_validators__(cls):
        yield cls._validate
        
    @classmethod
    def _validate(cls, value):
        
        if isinstance(value, cls):
            return value
        
        if  b'OK' == value:
            return cls


@dataclass(frozen=True)
class StreamID:
    timestamp: int
    counter: int

    @classmethod
    def __get_validators__(cls):
        yield cls._validate
        
    @classmethod
    def _validate(cls, value):
        
        if isinstance(value, cls):
            return value
        
        if  b'OK' == value:
            return cls