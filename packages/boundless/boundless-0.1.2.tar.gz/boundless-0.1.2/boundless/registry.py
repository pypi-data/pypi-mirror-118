from importlib import import_module
from inspect import isfunction
from pkgutil import walk_packages
from typing import Optional

from boundless.function import Function


class Registry:
    def __init__(self, package: object):
        self.offset = len(package.__name__) + 1  # Package name prefix.
        self.functions = {}
        self._walk(package)

    def find(self, path: str) -> Optional[Function]:
        scope = self.functions
        names = path.split(".")

        for name in names:
            if name not in scope:
                return None

            scope = scope[name]

        if not isinstance(scope, Function):
            return None

        return scope

    def _walk(self, package: object):
        if hasattr(package, "__path__"):
            for loader, name, is_pkg in walk_packages(package.__path__):
                self._walk(
                    import_module(
                        f"{package.__name__}.{name}",
                    )
                )

            return

        for item_name, item_object in package.__dict__.items():
            # Skip not callable e.g. classes with __call__.
            if not callable(item_object):
                continue

            # Skip not functions.
            if not isfunction(item_object):
                continue

            # Only local function, not imported ones.
            if item_object.__module__ != package.__name__:
                continue

            # Skip helper functions.
            if item_object.__name__.startswith("_"):
                continue

            # Remove package name prefix.
            self._add(
                f"{package.__name__}.{item_name}"[self.offset :],
                Function(
                    package.__name__[self.offset :],
                    item_name,
                    item_object,
                ),
            )

    def _add(self, path: str, function: Function):
        scope = self.functions
        names = path.split(".")

        for name in names[:-1]:
            if name not in scope:
                scope[name] = {}

            scope = scope[name]

        scope[names[-1]] = function
