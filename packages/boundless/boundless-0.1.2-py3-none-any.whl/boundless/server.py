from abc import ABC, abstractmethod
from logging import getLogger

from boundless.authorization import (
    AuthorizationBackend,
    DummyAuthorizationBackend,
    User,
)
from boundless.deferred import DeferredBackend, InMemoryDeferredBackend
from boundless.errors import (
    ApplicationError,
    AuthorizeError,
    DeserializeError,
    SerializeError,
    SignatureError,
    ValidateError,
)
from boundless.registry import Registry
from boundless.request import RpcRequest
from boundless.response import RpcResponse
from boundless.status import ServerStatus

logger = getLogger(__name__)


class ServerTransport(ABC):
    def __init__(self):
        self.handler = None

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass

    def set_handler(self, handler: callable) -> None:
        self.handler = handler


class Server(ABC):
    def __init__(
        self,
        transport: ServerTransport,
        functions: object,
        *,
        authorization_backend: AuthorizationBackend = DummyAuthorizationBackend(),
        deferred_backend: DeferredBackend = InMemoryDeferredBackend(),
    ):
        self.transport = transport
        self.transport.set_handler(self.on_request)
        self.registry = Registry(functions)
        self.authorization_backend = authorization_backend
        self.deferred_backend = deferred_backend

    async def start(self) -> None:
        await self.transport.start()

    async def stop(self) -> None:
        await self.transport.stop()

    async def cleanup(self) -> None:
        await self.deferred_backend.cleanup_results()

    async def on_request(self, request: RpcRequest) -> RpcResponse:
        user = await self.authorization_backend.get_user(request.headers.token)

        if user is None:
            return RpcResponse.error(ServerStatus.AUTHENTICATE_NO_USER)

        handler = self.registry.find(request.function)

        if handler is None:
            logger.error(f"Function {request.function} not found.")
            return RpcResponse.error(ServerStatus.HANDLER_NOT_EXIST)

        if not await user.has_capacity(handler.name):
            return RpcResponse.error(ServerStatus.THROTTLING_NO_CAPACITY)

        try:
            return RpcResponse.ok(
                await handler(
                    user=user,
                    positional=request.positional,
                    named=request.named,
                ),
            )
        except ApplicationError as error:
            return RpcResponse.error(
                ServerStatus.HANDLER_APPLICATION_ERROR,
                str(error),
            )
        except AuthorizeError as error:
            return RpcResponse.error(
                ServerStatus.AUTHORIZE_NO_PERMISSIONS,
                str(error),
            )
        except ValidateError as error:
            return RpcResponse.error(
                ServerStatus.HANDLER_VALIDATE_ERROR,
                str(error),
            )
        except DeserializeError as error:
            return RpcResponse.error(
                ServerStatus.HANDLER_DESERIALIZE_ERROR,
                str(error),
            )
        except SerializeError as error:
            return RpcResponse.error(
                ServerStatus.HANDLER_SERIALIZE_ERROR,
                str(error),
            )
        except SignatureError as error:
            return RpcResponse.error(
                ServerStatus.HANDLER_SIGNATURE_ERROR,
                str(error),
            )
        except BaseException:
            logger.exception("Exception while handling request.")
            return RpcResponse.error(
                ServerStatus.GENERAL_ERROR,
            )
