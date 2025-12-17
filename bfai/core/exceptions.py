class BFAIError(Exception):
    """Base exception for BFAI."""
    pass

class DataIngestionError(BFAIError):
    """Raised when data loading fails."""
    pass

class SchemaValidationError(BFAIError):
    """Raised when data does not match expected schema."""
    pass
