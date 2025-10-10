# Top-level package metadata and convenient re-exports.
__all__ = ["db"]
__version__ = "0.1.0"

# Optional: lift common DB funcs to karnai.*
from .db.db_api import (  # noqa: F401
    create,
    read_one,
    read_many,
    update,
    delete,
    pk_for,
)
