from abc import ABC, abstractmethod
from time import time
from uuid import uuid4


class DeferredBackend(ABC):
    @abstractmethod
    async def get_result(self, operation_id):
        pass

    @abstractmethod
    async def set_result(self, operation_id, *, result=None, done=False):
        pass

    @abstractmethod
    async def cleanup_results(self):
        pass

    @abstractmethod
    def generate_operation_id(self):
        pass


class InMemoryDeferredBackend(DeferredBackend):
    def __init__(self, timeout=600):
        self.results = {}
        self.timeout = timeout

    async def get_result(self, operation_id):
        if operation_id not in self.results:
            return None

        result = self.results[operation_id]
        del self.results[operation_id]
        return result

    async def set_result(self, operation_id, *, result=None, done=False):
        timestamp = time()

        if operation_id not in self.results:
            self.results[operation_id] = {
                "time": {
                    "start": timestamp,
                    "stop": None,
                }
            }

        self.results[operation_id]["result"] = result
        self.results[operation_id]["done"] = done

        if done:
            self.results[operation_id]["time"]["stop"] = timestamp

    async def cleanup_results(self):
        timestamp = time()
        operation_ids = []

        for operation_id, result in self.results.items():
            if result["time"]["stop"] is None:
                continue

            if timestamp - result["time"]["stop"] < self.timeout:
                continue

            operation_ids.append(operation_id)

        for operation_id in operation_ids:
            del self.results[operation_id]

    def generate_operation_id(self):
        return str(uuid4())
