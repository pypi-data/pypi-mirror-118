from argparse import ArgumentParser
from asyncio import run
from json import dumps
from urllib.parse import urlparse

from jmespath import search

from boundless.client import Client
from boundless.transport.client.aio_http_client_transport import AioHttpClientTransport


def parse_url(url):
    url = urlparse(url)
    return url.scheme, url.hostname, url.port, url.path.replace("/", "")


def parse_positional(positional):
    try:
        return eval(positional)
    except BaseException:
        return {}


def parse_named(named):
    try:
        return eval(named)
    except BaseException:
        return {}


async def main():
    parser = ArgumentParser()
    parser.add_argument(
        "url",
        type=str,
        help="Url in format http(s)://host:port/function",
    )
    parser.add_argument(
        "positional",
        type=str,
        nargs="?",
        default="[]",
        help="Function positional arguments as python list definition",
    )
    parser.add_argument(
        "named",
        type=str,
        nargs="?",
        default="{}",
        help="Function named arguments as python dict definition",
    )
    parser.add_argument(
        "--token",
        type=str,
        default=None,
        required=False,
        help="Authentication token",
    )
    parser.add_argument(
        "--timeout-connect",
        type=float,
        default=None,
        required=False,
        help="Connect timeout",
    )
    parser.add_argument(
        "--timeout-read",
        type=float,
        default=None,
        required=False,
        help="Read timeout",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=None,
        required=False,
        help="JMESPath expression to query data from response",
    )

    # Parse arguments.
    parameters = parser.parse_args()
    schema, host, port, function = parse_url(parameters.url)
    positional = parse_positional(parameters.positional)
    named = parse_positional(parameters.named)

    # Execute function.
    client = Client(
        AioHttpClientTransport(
            schema,
            host,
            port,
            timeout_connect=parameters.timeout_connect,
            timeout_read=parameters.timeout_read,
        ),
        token=parameters.token,
    )

    if not isinstance(positional, list):
        raise Exception("Type of function positional arguments is invalid.")

    if not isinstance(named, dict):
        raise Exception("Type of function named arguments is invalid.")

    result = await client(function, *positional, **named)

    # Query data.
    if parameters.query:
        if result is None:
            raise Exception("Query not applicable because result is empty.")

        print(search(parameters.query, result))
    else:
        print(dumps(result, indent=4))


run(main())
