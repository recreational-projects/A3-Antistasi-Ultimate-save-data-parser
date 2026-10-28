"""Define package-level fixtures for testing."""

from pathlib import Path
from typing import TYPE_CHECKING

import msgspec
import pytest

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode

_JSON_SAMPLE_PATH = Path(__file__).parent / "sample.json"
"""NB: this is a composite sample and won't be internally consistent."""


@pytest.fixture
def sample_str() -> str:
    """Return sample data `str`."""
    return _JSON_SAMPLE_PATH.read_text()


@pytest.fixture
def sample_dict(sample_str: str) -> JSONDictNode:
    """Return sample data `dict`."""
    return msgspec.json.decode(sample_str)
