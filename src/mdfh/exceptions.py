"""Custom exceptions for the MDFH set covering solver."""


class MDFHBaseException(Exception):
    """Base exception for all MDFH-related errors."""


class MDFHValidationError(MDFHBaseException):
    """Raised when input data for the MDFH solver is invalid."""


class MDFHSolverError(MDFHBaseException):
    """Raised when the MDFH solver reaches an unrecoverable state."""
