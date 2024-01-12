class NotFound(Exception):
    """Exception raised when a specific item is not found."""

    def __init__(self, message="Item not found"):
        self.message = f"{message} Not Found"
        super().__init__(self.message)


class FileProcessingError(Exception):
    """Exception raised when a file fails to process"""

    def __init__(self, message="Document Processing Fail"):
        self.message = f"{message} Not Found"
        super().__init__(self.message)