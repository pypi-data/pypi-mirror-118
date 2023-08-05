from abc import ABC, abstractmethod
from re import Pattern, compile
from typing import Any, Optional, Union


class Validator(ABC):
    def __init__(self):
        self.previous = None
        self.next = None
        self.value = None
        self.blocker = None

    def __or__(
        self,
        next: Union["Validator", Any],
    ) -> Union["Validator", Any]:
        """
        a = A(1)
        b = A(2)
        c = A(3)
        chain = a | b | c
        will be evaluated from left to right, so:
        a | b should return b
        b | c should return c
        """

        if isinstance(next, Validator):
            self.next = next
            self.next.previous = self
        else:
            self.next = Default(next)
            self.next.previous = self

        if not isinstance(self.next, Default):
            return self.next

        # Traversing list backward.
        previous = self

        while True:
            if previous.previous is None:
                return previous

            previous = previous.previous

    async def validate(
        self,
        value: Any,
    ) -> bool:
        # Reset blocker state.
        self.blocker = None

        # Traversing list forward.
        next = self

        while isinstance(next, Validator):
            if not await next._validate(value):
                self.blocker = str(next)
                return False

            next = next.next

        return True

    @property
    def default(self) -> Optional[Any]:
        next = self

        while next.next is not None:
            next = next.next

        return next.value

    @property
    def description(self) -> Optional[str]:
        if not isinstance(self, Description):
            return None

        return self.value

    @abstractmethod
    async def _validate(self, value: Any) -> bool:
        pass


class Description(Validator):
    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return "description"

    async def _validate(self, value: Any) -> bool:
        return True


class Default(Validator):
    def __init__(self, value: Any):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return "default"

    async def _validate(self, value: Any) -> bool:
        return True


class DefaultNotSpecified:
    pass


class MinValue(Validator):
    def __init__(
        self,
        min: int,
        *,
        is_equal: bool = True,
    ):
        super().__init__()
        self.min = min
        self.is_equal = is_equal

    def __str__(self) -> str:
        if self.is_equal:
            return f"value >= {self.min}"

        return f"value > {self.min}"

    async def _validate(self, value: Any) -> bool:
        if self.is_equal:
            return value >= self.min

        return value > self.min


class MaxValue(Validator):
    def __init__(
        self,
        max: int,
        *,
        is_equal: bool = True,
    ):
        super().__init__()
        self.max = max
        self.is_equal = is_equal

    def __str__(self) -> str:
        if self.is_equal:
            return f"value <= {self.max}"

        return f"value < {self.max}"

    async def _validate(self, value: Any) -> bool:
        if self.is_equal:
            return value <= self.max

        return value < self.max


class MinLength(Validator):
    def __init__(
        self,
        min: int,
        *,
        is_equal: bool = True,
    ):
        super().__init__()
        self.min = min
        self.is_equal = is_equal

    def __str__(self) -> str:
        if self.is_equal:
            return f"len(value) >= {self.min}"

        return f"len(value) > {self.min}"

    async def _validate(self, value: Any) -> bool:
        if self.is_equal:
            return len(value) >= self.min

        return len(value) > self.min


class MaxLength(Validator):
    def __init__(
        self,
        max: int,
        *,
        is_equal: bool = True,
    ):
        super().__init__()
        self.max = max
        self.is_equal = is_equal

    def __str__(self) -> str:
        if self.is_equal:
            return f"len(value) <= {self.max}"

        return f"len(value) < {self.max}"

    async def _validate(self, value: Any) -> bool:
        if self.is_equal:
            return len(value) <= self.max

        return len(value) < self.max


class Regex(Validator):
    def __init__(
        self,
        regex: Union[str, Pattern],
        *,
        is_match: bool = True,
    ):
        super().__init__()

        if isinstance(regex, str):
            self.regex = compile(regex)
        else:
            self.regex = regex

        self.is_match = is_match

    def __str__(self) -> str:
        if self.is_match:
            return f"value match {self.regex.pattern}"

        return f"value not match {self.regex.pattern}"

    async def _validate(self, value: Any) -> bool:
        if self.is_match:
            return self.regex.match(value)

        return not self.regex.match(value)
