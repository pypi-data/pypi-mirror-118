class ApiError(Exception):
    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class StatusError(Exception):
    def __init__(self, status_message):
        self._status_message = status_message

    def __str__(self):
        return self._status_message


class EngineError(Exception):
    def __init__(self, engine_message):
        self._engine_message = engine_message

    def __str__(self):
        return self._engine_message
