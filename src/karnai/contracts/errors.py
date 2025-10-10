class ContractError(Exception):
    """Raised when a contract is violated."""


class NotSupported(Exception):
    """Raised when an operation is not supported by the implementation."""


class DataError(Exception):
    """Raised for ingestion/schema/data failures."""
