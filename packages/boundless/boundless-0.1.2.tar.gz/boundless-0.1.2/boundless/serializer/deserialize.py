from dataclasses import _MISSING_TYPE, is_dataclass
from typing import Union, get_args, get_origin


class DeserializeError(BaseException):
    pass


def deserialize(expect_type, data):
    return to_object(expect_type, data)


def to_object(expect_type, data):
    lookup_type = expect_type

    if is_dataclass(expect_type):
        lookup_type = "dataclass"
    else:
        if get_origin(expect_type):
            lookup_type = get_origin(expect_type)

    if lookup_type not in mapping:
        raise DeserializeError(
            f'Type {lookup_type} not supported for data "{data}".',
        )

    return mapping[lookup_type](expect_type, data)


def to_none(expect_type, data):
    return None


def to_bool(expect_type, data):
    if not isinstance(data, bool):
        raise DeserializeError(
            f"Data {data} is not bool.",
        )

    return data


def to_int(expect_type, data):
    if not isinstance(data, int):
        raise DeserializeError(
            f"Data {data} is not int.",
        )

    return data


def to_float(expect_type, data):
    if not isinstance(data, float):
        raise DeserializeError(
            f"Data {data} is not float.",
        )

    return data


def to_str(expect_type, data):
    if not isinstance(data, str):
        raise DeserializeError(
            f"Data {data} is not str.",
        )

    return data


def to_list(expect_type, data):
    types = get_args(expect_type)

    if not isinstance(data, list):
        raise DeserializeError(
            f"Data {data} is not list, expect type {expect_type}.",
        )

    if not types:
        return data

    if len(types) != 1:
        raise DeserializeError(
            f"Invalid List annotation, data {data}.",
        )

    # fmt: off
    return list(
        [
            to_object(types[0], value)
            for value in data
        ]
    )
    # fmt: on


def to_tuple(expect_type, data):
    types = get_args(expect_type)

    if not isinstance(data, list):
        raise DeserializeError(f"Data {data} is not list, expect type {expect_type}.")

    if not types:
        return data

    # Tuple[T, ...]

    if len(types) == 2 and types[1] == Ellipsis:
        item_type = types[0]

        values = []

        for item_value in data:
            values.append(to_object(item_type, item_value))

        return tuple(values)

    # Tuple[T1, T2, T3, ...]

    if len(types) != len(data):
        raise DeserializeError(
            f"Tuple annotation length shoud be equal to data length, expect type {expect_type}, data {data}.",
        )

    values = []

    for item_type, item_value in zip(types, data):
        values.append(to_object(item_type, item_value))

    return tuple(values)


def to_dict(expect_type, data):
    types = get_args(expect_type)

    if not isinstance(data, dict):
        raise DeserializeError(
            f"Data {data} is not dict, expect type {expect_type}.",
        )

    if not types:
        return data

    if len(types) != 2:
        raise DeserializeError(
            f"Invalid Dict type annotation, data {data}.",
        )

    # fmt: off
    return dict(
        {
            to_object(types[0], key): to_object(types[1], value)
            for key, value in data.items()
        }
    )
    # fmt: on


def to_union(expect_type, data):
    types = get_args(expect_type)

    if not types:
        raise DeserializeError(
            f"Type annotation for Union not provided, data {data}.",
        )

    for object_type in types:
        try:
            return to_object(object_type, data)
        except DeserializeError:
            pass

    raise DeserializeError(
        f"None of Union types are suitable, expect type {expect_type}, data {data}.",
    )


def to_dataclass(expect_type, data):
    if not isinstance(data, dict):
        raise DeserializeError(
            f"Data {data} is not dict, expect type {expect_type}.",
        )

    values = {}

    for field_name, field_type in expect_type.__annotations__.items():
        if field_name in data:
            values[field_name] = to_object(field_type, data[field_name])
            continue

        field_default = expect_type.__dataclass_fields__[field_name].default

        if field_default == _MISSING_TYPE:
            raise DeserializeError(
                f"Dict key {field_name} not present, expect type {expect_type}, data {data}.",
            )

        values[field_name] = field_default

    return expect_type(**values)


mapping = {
    None: to_none,
    type(None): to_none,
    bool: to_bool,
    int: to_int,
    float: to_float,
    str: to_str,
    list: to_list,
    tuple: to_tuple,
    dict: to_dict,
    Union: to_union,
    "dataclass": to_dataclass,
}
