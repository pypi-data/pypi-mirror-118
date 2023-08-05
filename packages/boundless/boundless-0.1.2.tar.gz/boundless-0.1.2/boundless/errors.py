class SeamlessRpcError(Exception):
    pass


class DefinitionError(SeamlessRpcError):
    pass


class SignatureError(SeamlessRpcError):
    pass


class SerializeError(SeamlessRpcError):
    pass


class DeserializeError(SeamlessRpcError):
    pass


class ValidateError(SeamlessRpcError):
    pass


class AuthorizeError(SeamlessRpcError):
    pass


class ApplicationError(SeamlessRpcError):
    pass


class ClientError(SeamlessRpcError):
    def __init__(
        self,
        message: str = None,
        status_client: str = None,
        status_server: str = None,
    ):
        self.message = message
        self.status_client = status_client
        self.status_server = status_server

    def __str__(self):
        parts = []

        if self.message:
            parts.append(self.message + ".")

        if self.status_client:
            parts.append(f"Status client: {self.status_client}.")

        if self.status_server:
            parts.append(f"Status server: {self.status_server}.")

        if not parts:
            return ""

        return " ".join(parts)
