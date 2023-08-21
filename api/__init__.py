"""Unofficial Python wrapper for Tinytuya API."""
from importlib.metadata import version

from .client import Rainpoint

try:
    __version__ = version(__name__)
except Exception:  # pylint: disable=broad-except
    pass

__all__ = ["Rainpoint"]
