from abc import ABC, abstractmethod
from typing import Any, Dict

from boundless.permission import PermissionChecker


class User(ABC):
    @abstractmethod
    async def has_permission(
        self,
        checker: PermissionChecker,
        **kwargs: Dict[str, Any],
    ) -> bool:
        pass

    @abstractmethod
    async def has_capacity(
        self,
        function: str,
    ) -> bool:
        pass


class AuthorizationBackend(ABC):
    @abstractmethod
    async def get_user(
        self,
        token: str,
    ) -> User:
        pass


class DummyUser(User):
    async def has_permission(
        self,
        checker: PermissionChecker,
        **kwargs: Dict[str, Any],
    ) -> bool:
        return True

    async def has_capacity(
        self,
        function: str,
    ) -> bool:
        return True


class DummyAuthorizationBackend(AuthorizationBackend):
    async def get_user(
        self,
        token: str,
    ) -> User:
        return DummyUser()
