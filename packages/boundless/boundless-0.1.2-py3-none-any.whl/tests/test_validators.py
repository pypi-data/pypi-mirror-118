from pytest import mark
from boundless.validators import (
    Default,
    Description,
    MaxLength,
    MaxValue,
    MinLength,
    MinValue,
    Regex,
)


@mark.asyncio
async def test_default():
    chain = Default(0)
    assert await chain.validate(0) == True
    assert await chain.validate(1) == True


@mark.asyncio
async def test_description():
    chain = Description("description")
    assert chain.description == "description"
    assert await chain.validate(0) == True
    assert await chain.validate(1) == True

    chain = Default(0)
    assert chain.description == None

    chain = MinValue(0)
    assert chain.description == None

    chain = MinValue(0) | Default(0)
    assert chain.description == None

    chain = Description("description") | MinValue(0) | Default(0)
    assert chain.description == "description"
    assert await chain.validate(0) == True


@mark.asyncio
async def test_min_value():
    validator = MinValue(0, is_equal=True)
    assert str(validator) == "value >= 0"

    chain = MinValue(0, is_equal=True)
    assert await chain.validate(-1) == False
    assert chain.blocker == "value >= 0"
    assert await chain.validate(0) == True
    assert chain.blocker == None
    assert await chain.validate(1) == True
    assert chain.blocker == None

    validator = MinValue(0, is_equal=False)
    assert str(validator) == "value > 0"

    chain = MinValue(0, is_equal=False)
    assert await chain.validate(-1) == False
    assert chain.blocker == "value > 0"
    assert await chain.validate(0) == False
    assert chain.blocker == "value > 0"
    assert await chain.validate(1) == True
    assert chain.blocker == None


@mark.asyncio
async def test_max_value():
    validator = MaxValue(1, is_equal=True)
    assert str(validator) == "value <= 1"

    chain = MaxValue(1, is_equal=True)
    assert await chain.validate(0) == True
    assert chain.blocker == None
    assert await chain.validate(1) == True
    assert chain.blocker == None
    assert await chain.validate(2) == False
    assert chain.blocker == "value <= 1"

    validator = MaxValue(1, is_equal=False)
    assert str(validator) == "value < 1"

    chain = MaxValue(1, is_equal=False)
    assert await chain.validate(0) == True
    assert chain.blocker == None
    assert await chain.validate(1) == False
    assert chain.blocker == "value < 1"
    assert await chain.validate(2) == False
    assert chain.blocker == "value < 1"


@mark.asyncio
async def test_min_length():
    validator = MinLength(0, is_equal=True)
    assert str(validator) == "len(value) >= 0"

    chain = MinLength(1, is_equal=True)
    assert await chain.validate("") == False
    assert chain.blocker == "len(value) >= 1"
    assert await chain.validate("a") == True
    assert chain.blocker == None
    assert await chain.validate("ab") == True
    assert chain.blocker == None

    validator = MinLength(0, is_equal=False)
    assert str(validator) == "len(value) > 0"

    chain = MinLength(1, is_equal=False)
    assert await chain.validate("") == False
    assert chain.blocker == "len(value) > 1"
    assert await chain.validate("a") == False
    assert chain.blocker == "len(value) > 1"
    assert await chain.validate("ab") == True
    assert chain.blocker == None


@mark.asyncio
async def test_max_length():
    validator = MaxLength(1, is_equal=True)
    assert str(validator) == "len(value) <= 1"

    chain = MaxLength(1, is_equal=True)
    assert await chain.validate("") == True
    assert chain.blocker == None
    assert await chain.validate("a") == True
    assert chain.blocker == None
    assert await chain.validate("ab") == False
    assert chain.blocker == "len(value) <= 1"

    validator = MaxLength(1, is_equal=False)
    assert str(validator) == "len(value) < 1"

    chain = MaxLength(1, is_equal=False)
    assert await chain.validate("") == True
    assert chain.blocker == None
    assert await chain.validate("a") == False
    assert chain.blocker == "len(value) < 1"
    assert await chain.validate("ab") == False
    assert chain.blocker == "len(value) < 1"


@mark.asyncio
async def test_regex():
    chain = Regex(r"[a-z]+", is_match=True)
    assert await chain.validate("a") == True
    assert chain.blocker == None
    assert await chain.validate("1") == False
    assert chain.blocker == "value match [a-z]+"

    chain = Regex(r"[a-z]+", is_match=False)
    assert await chain.validate("a") == False
    assert chain.blocker == "value not match [a-z]+"
    assert await chain.validate("1") == True
    assert chain.blocker == None


@mark.asyncio
async def test_chain_link():
    a = MinValue(0)
    assert a.previous == None
    assert a.next == None

    a = MinValue(0)
    b = Default(1)
    chain = a | b
    assert chain == a
    assert a.previous == None
    assert a.next == b
    assert b.previous == a
    assert b.next == None

    a = MinValue(0)
    b = MinValue(1)
    c = Default(2)
    chain = a | b | c
    assert chain == a
    assert a.previous == None
    assert a.next == b
    assert b.previous == a
    assert b.next == c
    assert c.previous == b
    assert c.next == None


@mark.asyncio
async def test_chain_validate():
    chain = MinValue(0) | MaxValue(2) | 0
    assert chain.default == 0
    assert await chain.validate(-1) == False
    assert chain.blocker == "value >= 0"
    assert await chain.validate(0) == True
    assert chain.blocker == None
    assert await chain.validate(1) == True
    assert chain.blocker == None
    assert await chain.validate(2) == True
    assert chain.blocker == None
    assert await chain.validate(3) == False
    assert chain.blocker == "value <= 2"


@mark.asyncio
async def test_chain_default():
    chain = MinValue(0)
    assert chain.default == None

    chain = MinValue(0) | 0
    assert chain.default == 0

    chain = Default(0)
    assert chain.default == 0

    chain = MinValue(0) | Default(0)
    assert chain.default == 0
