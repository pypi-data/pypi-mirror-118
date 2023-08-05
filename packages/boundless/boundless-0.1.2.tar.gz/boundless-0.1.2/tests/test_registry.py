from pytest import mark
from boundless.registry import Registry

from tests import functions


# TODO: tests
@mark.asyncio
async def test_find():
    registry = Registry(functions)
    function = registry.find("one.two.three")
    assert await function() == "four"
