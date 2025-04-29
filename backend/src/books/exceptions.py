class BusinessLogicException(Exception):
    """Base exception for business logic errors."""
    pass


class ResourceNotFoundException(BusinessLogicException):
    """Raised when a required resource is not found."""
    def __init__(self, resource_name: str, resource_id: str):
        self.resource_name = resource_name
        self.resource_id = resource_id
        super().__init__(f"{resource_name} with ID '{resource_id}' not found.")


class ResourceAlreadyExistsException(BusinessLogicException):
    """Raised when a resource already exists."""
    def __init__(self, resource_name: str, resource_id: str):
        self.resource_name = resource_name
        self.resource_id = resource_id
        super().__init__(f"{resource_name} with ID '{resource_id}' already exists.")


class ResourceAlreadyDeletedException(BusinessLogicException):
    """Raised when a resource already deleted."""
    def __init__(self):
        super().__init__(f"Resource already deleted.")

class NoAvailableColorException(Exception):
    """Raised when no more available colors exist"""
    def __init__(self):
        super().__init__(f"No available color.")

