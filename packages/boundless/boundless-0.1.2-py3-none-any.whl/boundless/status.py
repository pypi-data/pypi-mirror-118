class ServerStatus:
    OK = "ok"
    GENERAL_ERROR = "general_error"
    SCHEMA_ERROR = "schema_error"

    AUTHENTICATE_NO_USER = "authenticate_no_user"
    AUTHORIZE_NO_PERMISSIONS = "authorize_no_permissions"

    THROTTLING_NO_CAPACITY = "throttling_no_capacity"

    HANDLER_NOT_EXIST = "handler_not_exist"
    HANDLER_SIGNATURE_ERROR = "handler_signature_error"
    HANDLER_SERIALIZE_ERROR = "handler_serialize_error"
    HANDLER_DESERIALIZE_ERROR = "handler_deserialize_error"
    HANDLER_VALIDATE_ERROR = "handler_validate_error"
    HANDLER_APPLICATION_ERROR = "handler_application_error"


class ClientStatus:
    GENERAL_ERROR = "general_error"
    CONNECTION_ERROR = "connection_error"
    RESOLUTION_ERROR = "resolution_error"
    TIMEOUT_ERROR = "timeout_error"
    SCHEMA_ERROR = "schema_error"
