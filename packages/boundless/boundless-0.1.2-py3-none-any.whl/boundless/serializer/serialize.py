from dataclasses import is_dataclass
from inspect import _empty
from typing import Union, get_args, get_origin


class SerializeError(BaseException):
    pass


def serialize(expect_type, data):
    return from_object(expect_type, data)


def from_object(expect_type, data):
    lookup_type = expect_type

    if is_dataclass(expect_type):
        lookup_type = "dataclass"
    else:
        if get_origin(expect_type):
            lookup_type = get_origin(expect_type)

    if lookup_type not in mapping:
        raise SerializeError(
            f'Type {lookup_type} not supported for data "{data}".',
        )

    return mapping[lookup_type](expect_type, data)


def from_none(expect_type, data):
    return None


def from_bool(expect_type, data):
    if not isinstance(data, bool):
        raise SerializeError(
            f"Data {data} is not bool.",
        )

    return data


def from_int(expect_type, data):
    if not isinstance(data, int):
        raise SerializeError(
            f"Data {data} is not int.",
        )

    return data


def from_float(expect_type, data):
    if not isinstance(data, float):
        raise SerializeError(
            f"Data {data} is not float.",
        )

    return data


def from_str(expect_type, data):
    if not isinstance(data, str):
        raise SerializeError(
            f"Data {data} is not str.",
        )

    return data


def from_list(expect_type, data):
    types = get_args(expect_type)

    if not isinstance(data, list):
        raise SerializeError(
            f"Data {data} is not list, expect type {expect_type}.",
        )

    if not types:
        return data

    if len(types) != 1:
        raise SerializeError(
            f"Invalid List annotation, data {data}.",
        )

    # fmt: off
    return list(
        [
            from_object(types[0], value)
            for value in data
        ]
    )
    # fmt: on


def from_tuple(expect_type, data):
    types = get_args(expect_type)

    if not isinstance(data, list):
        raise SerializeError(f"Data {data} is not list, expect type {expect_type}.")

    if not types:
        return data

    # Tuple[T, ...]

    if len(types) == 2 and types[1] == Ellipsis:
        item_type = types[0]

        values = []

        for item_value in data:
            values.append(from_object(item_type, item_value))

        return tuple(values)

    # Tuple[T1, T2, T3, ...]

    if len(types) != len(data):
        raise SerializeError(
            f"Tuple annotation length shoud be equal to data length, expect type {expect_type}, data {data}.",
        )

    values = []

    for item_type, item_value in zip(types, data):
        values.append(from_object(item_type, item_value))

    return tuple(values)


def from_dict(expect_type, data):
    types = get_args(expect_type)

    if not isinstance(data, dict):
        raise SerializeError(
            f"Data {data} is not dict, expect type {expect_type}.",
        )

    if not types:
        return data

    if len(types) != 2:
        raise SerializeError(
            f"Invalid Dict type annotation, data {data}.",
        )

    # fmt: off
    return dict(
        {
            from_object(types[0], key): from_object(types[1], value)
            for key, value in data.items()
        }
    )
    # fmt: on


def from_union(expect_type, data):
    types = get_args(expect_type)

    if not types:
        raise SerializeError(
            f"Type annotation for Union not provided, data {data}.",
        )

    for object_type in types:
        try:
            return from_object(object_type, data)
        except SerializeError:
            pass

    raise SerializeError(
        f"None of Union types are suitable, expect type {expect_type}, data {data}.",
    )


def from_dataclass(expect_type, data):
    if not is_dataclass(data):
        raise SerializeError(
            f"Data {data} is not dataclass, expect type {expect_type}.",
        )

    # fmt: off
    return dict({
        field_name: from_object(
            field_type,
            getattr(data, field_name),
        )
        for field_name, field_type in expect_type.__annotations__.items()
    })
    # fmt: on


mapping = {
    None: from_none,
    type(None): from_none,
    _empty: from_none,
    bool: from_bool,
    int: from_int,
    float: from_float,
    str: from_str,
    list: from_list,
    tuple: from_tuple,
    dict: from_dict,
    Union: from_union,
    "dataclass": from_dataclass,
}
