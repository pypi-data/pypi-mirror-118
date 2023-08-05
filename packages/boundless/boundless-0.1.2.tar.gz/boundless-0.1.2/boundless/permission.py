from abc import ABC, abstractmethod


class PermissionChecker(ABC):
    @abstractmethod
    async def __call__(self, user: "User", **kwargs):
        pass


class DummyPermissionChecker(PermissionChecker):
    async def __call__(self, user: "User", **kwargs):
        return True


def permission(checker: PermissionChecker):
    def _wrapper(function):
        setattr(
            function,
            "__permission__",
            checker,
        )
        return function

    return _wrapper
