from dataclasses import dataclass
from typing import Union


@dataclass
class RpcRequestHeaders:
    token: str = None
    deferred: bool = False


@dataclass
class RpcRequest:
    headers: RpcRequestHeaders
    function: str
    positional: list
    named: dict
