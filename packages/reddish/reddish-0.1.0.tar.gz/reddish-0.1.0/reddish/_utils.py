from typing import Union, Iterable
from itertools import islice
from pydantic.json import pydantic_encoder
import json

def to_resp_array(*parts: bytes):
    """Builds a RESP request"""
    
    request = bytearray(b'*%d\r\n' % len(parts))

    for part in parts:
        request += b'$%d\r\n' % len(part)
        request +=b'%b\r\n' % part

    return request

def to_bytes(arg: Union[str, bytes]):
    if isinstance(arg, bytes):
        return arg
    elif isinstance(arg, str):
        return arg.encode('utf-8')
    else:
        raise TypeError(f"'{arg}' cannot be cast into bytes.")

def partition(iterable: Iterable, lenghts=Iterable[int]):
    iterator = iter(iterable)
    for length in lenghts:
        yield tuple(islice(iterator, length))

def json_dumps(data):
    return json.dumps(data, default=pydantic_encoder)