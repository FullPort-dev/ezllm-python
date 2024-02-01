from requests import Response


class NotFound(Exception):
    """Exception raised when a specific item is not found."""

    def __init__(self, message="Item not found"):
        self.message = f"{message} Not Found"
        super().__init__(self.message)


class FileProcessingError(Exception):
    """Exception raised when a file fails to process"""

    def __init__(self, message="Document Processing Fail"):
        self.message = f"{message}"
        super().__init__(self.message)


class InsufficientFundsError(Exception):
    """Exception raised when a workspace is out of funds"""
    def __init__(self, message="Insufficient Funds"):
        self.message = f"{message}"
        super().__init__(self.message)

class InternalServerError(Exception):
    pass

def handle_request_errors(response: Response):
    if response.status_code == 402:
        raise InsufficientFundsError("Insufficient Funds")
    elif response.status_code == 500:
        raise InternalServerError("Internal Server Error")
    