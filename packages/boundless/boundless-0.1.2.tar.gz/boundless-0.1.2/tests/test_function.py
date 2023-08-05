from typing import Tuple

from pytest import mark, raises
from boundless.errors import SignatureError, ValidateError
from boundless.function import Function
from boundless.validators import Default, MinValue


# TODO: tests
@mark.asyncio
async def test_positional_with_default():
    async def f(x: int = MinValue(1) | Default(1)) -> int:
        return x

    function = Function("f", f)

    # With positional arguments.
    await function(positional=[1]) == 1

    # With named arguments.
    with raises(
        SignatureError,
        # match="Function f call with invalid named parameters {'x': 1}.",
    ):
        await function(named={"x": 1})

    # Without arguments.
    await function() == 1

    # With invalid named argument value.
    with raises(
        ValidateError,
        # match="Function f call with invalid parameter value, parameter x, value 0, stoped at validator condition value >= 1.",
    ):
        await function(positional=[0])


@mark.asyncio
async def test_named_with_default():
    async def f(*, x: int = MinValue(1) | Default(1)) -> int:
        return x

    function = Function("f", f)

    # With positional arguments.
    with raises(
        SignatureError,
        # match="Function f call with invalid position parameters [1].",
    ):
        await function(positional=[1])

    # With named arguments.
    await function(named={"x": 1}) == 1

    # Without arguments.
    await function() == 1

    # With invalid named argument value.
    with raises(
        ValidateError,
        # match="Function f call with invalid parameter value, parameter x, value 0, stoped at validator condition value >= 1.",
    ):
        await function(named={"x": 0})
