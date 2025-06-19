class oxiusException(Exception):
    pass


class HTTPException(oxiusException):
    def __init__(self, message="HTTP error occurred", status=None):
        self.message = message
        self.status = status
        super().__init__(f"{message}" + (f" [Status: {status}]" if status else ""))


class ConnectionException(oxiusException):
    def __init__(self, message="Connection failed"):
        super().__init__(message)


class TimeoutException(oxiusException):
    def __init__(self, message="Request timed out"):
        super().__init__(message)


class DecodeException(oxiusException):
    def __init__(self, message="Failed to decode response"):
        super().__init__(message)
