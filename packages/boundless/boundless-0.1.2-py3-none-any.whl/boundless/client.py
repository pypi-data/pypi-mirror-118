from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any

logger = getLogger(__name__)


class ClientTransport(ABC):
    @abstractmethod
    async def __call__(self, function: str, *args, **kwargs) -> Any:
        pass


class Client:
    def __init__(
        self,
        transport: ClientTransport,
        *,
        token: str = None,
    ):
        self._transport = transport
        self._token = token

    def __getattr__(self, attribute: str) -> Any:
        return CallChain(self, attribute)

    async def __call__(
        self,
        function: str,
        *args,
        timeout_connect: float = None,
        timeout_read: float = None,
        **kwargs,
    ) -> Any:
        return await self._transport(
            self._token,
            function,
            *args,
            timeout_connect=timeout_connect,
            timeout_read=timeout_read,
            **kwargs,
        )


class CallChain:
    def __init__(self, client: Client, name: str):
        self.client = client
        self.name = name

    def __getattr__(self, attribute: str) -> Any:
        return CallChain(self.client, f"{self.name}.{attribute}")

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.client(self.name, *args, **kwargs)
