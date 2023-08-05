from asyncio import TimeoutError
from logging import getLogger
from typing import Any

from aiohttp import ClientConnectionError, ClientSession
from boundless.client import ClientTransport
from boundless.errors import ClientError
from boundless.status import ClientStatus, ServerStatus

logger = getLogger(__name__)


class AioHttpClientTransport(ClientTransport):
    def __init__(
        self,
        schema: str,
        host: str,
        port: int,
        *,
        timeout_connect: float = None,
        timeout_read: float = None,
    ):
        self.schema = schema
        self.host = host
        self.port = port
        self.timeout_connect = timeout_connect
        self.timeout_read = timeout_read

    async def __call__(
        self,
        token: str,
        function: str,
        *args,
        timeout_connect: float = None,
        timeout_read: float = None,
        **kwargs,
    ) -> Any:
        # Json.
        json = {
            "headers": {},
            "function": function,
            "arguments": {
                "positional": [],
                "named": {},
            },
        }

        # Headers.
        if token:
            json["headers"]["token"] = token

        # Arguments.
        if args:
            json["arguments"]["positional"] = args

        if kwargs:
            json["arguments"]["named"] = kwargs

        # Select timeouts.
        if timeout_connect is None:
            timeout_connect = self.timeout_connect

        if timeout_read is None:
            timeout_read = self.timeout_read

        # Request.
        try:
            async with ClientSession(
                conn_timeout=timeout_connect,
                read_timeout=timeout_read,
            ) as client:
                response = await client.post(
                    f"{self.schema}://{self.host}:{self.port}",
                    json=json,
                )
                response = await response.json()

                if "status" not in response:
                    raise ClientError(
                        status_client=ClientStatus.SCHEMA_ERROR,
                    )

                if "details" not in response:
                    raise ClientError(
                        status_client=ClientStatus.SCHEMA_ERROR,
                    )

                if "result" not in response:
                    raise ClientError(
                        status_client=ClientStatus.SCHEMA_ERROR,
                    )

                if response["status"] != ServerStatus.OK:
                    raise ClientError(
                        status_server=response["status"],
                        message=response["details"],
                    )

                return response["result"]
        except ClientError:
            raise
        except ClientConnectionError as error:
            raise ClientError(
                message=str(error),
                status_client=ClientStatus.CONNECTION_ERROR,
            )
        except TimeoutError as error:
            raise ClientError(
                message=str(error),
                status_client=ClientStatus.TIMEOUT_ERROR,
            )
        except BaseException as error:
            logger.exception("Exception while connecting server.")
            raise ClientError(
                message=str(error),
                status_client=ClientStatus.GENERAL_ERROR,
            )
