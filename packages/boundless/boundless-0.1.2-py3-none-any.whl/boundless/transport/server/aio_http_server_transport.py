from typing import List

from aiohttp.web import Application, AppRunner
from aiohttp.web import Request as HttpRequest
from aiohttp.web import Response as HttpResponse
from aiohttp.web import TCPSite, json_response, options, post
from boundless.request import RpcRequest, RpcRequestHeaders
from boundless.response import RpcResponse
from boundless.server import ServerTransport
from boundless.status import ServerStatus


class AioHttpServerTransport(ServerTransport):
    def __init__(self, host: str, port: int, middlewares: List[callable] = None):
        self.host = host
        self.port = port

        if middlewares is None:
            middlewares = []

        self.application = Application(middlewares=middlewares)
        self.application.add_routes((post("/", self.index),))
        self.application.add_routes((options("/", self.options),))

        super().__init__()

    async def start(self) -> None:
        # Create runner.
        runner = AppRunner(self.application)
        await runner.setup()

        # Create tcp site.
        site = TCPSite(runner, self.host, self.port)
        await site.start()

    async def stop(self) -> None:
        pass

    async def index(self, request: HttpRequest) -> HttpResponse:
        headers = {}

        if "Origin" in request.headers:
            headers["Access-Control-Allow-Origin"] = request.headers["Origin"]

        try:
            data = await request.json()
        except BaseException:
            return to_http_response(
                RpcResponse.error(
                    ServerStatus.SCHEMA_ERROR,
                ),
                headers,
            )

        if "headers" not in data:
            return to_http_response(
                RpcResponse.error(
                    ServerStatus.SCHEMA_ERROR,
                ),
                headers,
            )

        if "function" not in data:
            return to_http_response(
                RpcResponse.error(
                    ServerStatus.SCHEMA_ERROR,
                ),
                headers,
            )

        if "arguments" not in data:
            return to_http_response(
                RpcResponse.error(
                    ServerStatus.SCHEMA_ERROR,
                ),
                headers,
            )

        if "positional" not in data["arguments"] or not isinstance(
            data["arguments"]["positional"],
            list,
        ):
            return to_http_response(
                RpcResponse.error(
                    ServerStatus.SCHEMA_ERROR,
                ),
                headers,
            )

        if "named" not in data["arguments"] or not isinstance(
            data["arguments"]["named"],
            dict,
        ):
            return to_http_response(
                RpcResponse.error(
                    ServerStatus.SCHEMA_ERROR,
                ),
                headers,
            )

        if "token" in data["headers"]:
            token = data["headers"]["token"]
        else:
            token = None

        if "deferred" in data["headers"]:
            deferred = data["headers"]["deferred"]
        else:
            deferred = None

        rpc_request = RpcRequest(
            RpcRequestHeaders(
                token,
                deferred,
            ),
            data["function"],
            data["arguments"]["positional"],
            data["arguments"]["named"],
        )
        return to_http_response(
            await self.handler(rpc_request),
            headers,
        )

    async def options(self, request: HttpRequest) -> HttpResponse:
        headers = {
            "Access-Control-Allow-Credentials": "false",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "*",
        }

        if "Origin" in request.headers:
            headers["Access-Control-Allow-Origin"] = request.headers["Origin"]

        return json_response({}, headers=headers)


def to_http_response(rpc_response: RpcResponse, headers: dict = None) -> HttpResponse:
    if headers is None:
        headers = {}

    if rpc_response.status == ServerStatus.OK:
        status = 200
    else:
        status = 400

    return json_response(
        {
            "status": rpc_response.status,
            "details": rpc_response.details,
            "result": rpc_response.result,
        },
        status=status,
        headers=headers,
    )
