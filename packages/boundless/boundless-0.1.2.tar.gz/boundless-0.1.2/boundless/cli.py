from argparse import ArgumentParser
from asyncio import run
from typing import Optional

from .function import Function
from .registry import Registry


def cli(
    package: object,
    *,
    program: Optional[str] = None,
    description: Optional[str] = None,
):
    parse(
        build_commands(
            Registry(package).functions,
        ),
        program,
        description,
    )


def build_commands(functions):
    commands = []

    for key, value in functions.items():
        if isinstance(value, Function):
            commands.append(value)
            continue

        commands.append(
            {
                "suffix": key,
                "commands": build_commands(value),
            }
        )

    return commands


def parse(commands, program, description):
    # Create parser.
    parser = ArgumentParser(
        prog=program,
        description=description,
    )
    build_subparsers(parser, commands)

    # Parse arguments.
    arguments = parser.parse_args()

    if not hasattr(arguments, "handler"):
        return

    parameters = dict(vars(arguments))
    parameters.pop("handler")

    # Call handler.
    run(arguments.handler(named=parameters))


def build_subparsers(parser, commands):
    subparsers = parser.add_subparsers()

    for command in commands:
        if isinstance(command, dict):
            subparser = subparsers.add_parser(
                command["suffix"],
            )
            build_subparsers(subparser, command["commands"])
            continue

        subparser = subparsers.add_parser(
            command.name.replace("_", "-"),
            help=command.function.__doc__,
        )

        for parameter in command.parameters_named.values():
            subparser.add_argument(
                "--" + parameter.name.replace("_", "-"),
                type=parameter.type,
                help=parameter.validator.description,
            )

        subparser.set_defaults(handler=command)
