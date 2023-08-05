from dataclasses import dataclass
from inspect import Parameter as SignatureParameter
from inspect import _empty, iscoroutinefunction, signature
from logging import getLogger
from typing import Any, Callable, Optional

from boundless.authorization import User
from boundless.errors import (
    AuthorizeError,
    DefinitionError,
    SignatureError,
    ValidateError,
)
from boundless.serializer import (
    DeserializeError,
    SerializeError,
    deserialize,
    serialize,
)
from boundless.validators import Default, DefaultNotSpecified, Validator

logger = getLogger(__name__)


@dataclass
class Parameter:
    name: str
    type: Any
    validator: Any


class Function:
    def __init__(self, path: str, name: str, function: Callable):
        assert iscoroutinefunction(function), f"Function {name} is not coroutine."

        self.path = path
        self.name = name
        self.function = function
        self.signature = signature(function)
        self.parameters_all = {}
        self.parameters_positional = {}
        self.parameters_named = {}
        self.result_type = self.signature.return_annotation

        for _, parameter in self.signature.parameters.items():
            if parameter.name == "user":
                continue

            if parameter.kind not in (
                SignatureParameter.POSITIONAL_ONLY,
                SignatureParameter.POSITIONAL_OR_KEYWORD,
                SignatureParameter.KEYWORD_ONLY,
            ):
                raise DefinitionError(
                    f"Parameter {parameter.name} should be either positional or keyword."
                )

            # TODO: a = DefaultNotSpecified()
            if isinstance(parameter.default, _empty):
                # def foo(a)
                validator = DefaultNotSpecified()
            else:
                if isinstance(parameter.default, Validator):
                    # def foo(a = Default(0))
                    # def foo(a = MinValue(0))
                    # def foo(a = MinValue(0) | 0)
                    # def foo(a = MinValue(0) | Default(0))
                    # def foo(a = Description("description") | MinValue(0) | Default(0))
                    validator = parameter.default
                else:
                    # def foo(a = 0)
                    validator = Default(parameter.default)

            # All kind of parameters.
            self.parameters_all[parameter.name] = Parameter(
                parameter.name,
                parameter.annotation,
                validator,
            )

            # Positional parameters.
            if parameter.kind in (
                SignatureParameter.POSITIONAL_ONLY,
                SignatureParameter.POSITIONAL_OR_KEYWORD,
            ):
                self.parameters_positional[parameter.name] = Parameter(
                    parameter.name,
                    parameter.annotation,
                    validator,
                )

            # Named parameters.
            if parameter.kind == SignatureParameter.KEYWORD_ONLY:
                self.parameters_named[parameter.name] = Parameter(
                    parameter.name,
                    parameter.annotation,
                    validator,
                )

    async def __call__(
        self,
        user: Optional[User] = None,
        positional: Optional[list] = None,
        named: Optional[dict] = None,
        is_serialize: bool = False,
    ) -> Any:
        # Prepare parameters.
        data = {}

        try:
            data.update(self._prepare_positional(positional))
            data.update(self._prepare_named(named))
        except SignatureError:
            logger.exception("Function call with invalid signature.")
            raise

        # Deserialize parameters.
        arguments = {}

        for key in self.parameters_all.keys():
            try:
                arguments[key] = deserialize(
                    self.parameters_all[key].type,
                    data[key],
                )
            except DeserializeError:
                logger.exception(
                    f"Function {self.path}.{self.name} call with invalid parameters schema {self.parameters_all}.",
                )
                raise

        # Validate parameters.
        for key in self.parameters_all.keys():
            validator = self.parameters_all[key].validator
            value = arguments[key]

            if not await validator.validate(value):
                raise ValidateError(
                    f"Function {self.path}.{self.name} call with invalid parameter value, "
                    f"parameter {key}, value {value}, stoped at validator condition {validator.blocker}.",
                )

        # Check authorization.
        if user is not None and self.permission is not None and not await user.has_permission(
            self.permission, **arguments
        ):
            raise AuthorizeError("User has not permission to access resource.")

        # Call function.
        try:
            if user is None:
                result = await self.function(**arguments)
            else:
                result = await self.function(user=user, **arguments)
        except ValidateError:
            logger.exception(
                f"Validate error while call function {self.path}.{self.name}.",
            )
            raise

        if not is_serialize:
            return result

        # Serialize result.
        try:
            # TODO: result_type -> None, result = list.
            return serialize(self.result_type, result)
        except SerializeError:
            logger.exception(
                f"Function {self.path}.{self.name} result can not be serialized {result}.",
            )
            raise

    @property
    def permission(self):
        return getattr(self.function, "__permission__", None)

    def _prepare_positional(self, positional: Optional[list] = None) -> dict:
        # Enrich input.
        if positional is None:
            positional = []

        # Validate type.
        if not isinstance(positional, list):
            raise SignatureError(
                f"Function {self.path}.{self.name} call with invalid positional parameters, it should be list, {type(positional)} passed.",
            )

        data = {}
        data_length = len(positional)

        # Validate names.
        if data_length > len(self.parameters_positional):
            raise SignatureError(
                f"Function {self.path}.{self.name} call with invalid position parameters {positional}.",
            )

        # Fill data.
        for i, key in enumerate(self.parameters_positional.keys()):
            # Passed param.
            if i < data_length:
                data[key] = positional[i]
                continue

            # Default.
            default = self.parameters_positional[key].validator.default

            if isinstance(default, DefaultNotSpecified):
                raise SignatureError(
                    f"Function {self.path}.{self.name} call with invalid position parameters {positional}.",
                )

            data[key] = default

        return data

    def _prepare_named(self, named: Optional[dict] = None) -> dict:
        # Enrich input.
        if named is None:
            named = {}

        # Validate type.
        if not isinstance(named, dict):
            raise SignatureError(
                f"Function {self.path}.{self.name} call with invalid named parameters, it should be dict, {type(named)} passed.",
            )

        # Validate names.
        data = {}

        if set(named.keys()) - set(self.parameters_named.keys()):
            raise SignatureError(
                f"Function {self.path}.{self.name} call with invalid named parameters {named}.",
            )

        # Fill data.
        for key in self.parameters_named.keys():
            # Passed param.
            if key in named:
                data[key] = named[key]
                continue

            # Default.
            default = self.parameters_named[key].validator.default

            if isinstance(default, DefaultNotSpecified):
                raise SignatureError(
                    f"Function {self.path}.{self.name} call with invalid named parameters {named}.",
                )

            data[key] = default

        return data
