from dataclasses import dataclass
from typing import Any

from boundless.status import ServerStatus


@dataclass
class RpcResponse:
    status: str
    details: str
    result: Any

    @staticmethod
    def ok(result: Any) -> "RpcResponse":
        return RpcResponse(ServerStatus.OK, None, result)

    @staticmethod
    def error(status: str, details: str = None) -> "RpcResponse":
        return RpcResponse(status, details, None)
