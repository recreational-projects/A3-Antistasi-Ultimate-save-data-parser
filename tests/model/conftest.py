"""Define package-level fixtures for testing."""

from pathlib import Path
from typing import Any

import msgspec
import pytest

_JSON_SAMPLE_PATH = Path(__file__).parent / "sample.json"
"""NB: this is a composite sample and won't be internally consistent."""

type DictNode = dict[str, Any]


@pytest.fixture
def sample_str() -> str:
    """Return sample data `str`."""
    return _JSON_SAMPLE_PATH.read_text()


@pytest.fixture
def sample_dict(sample_str: str) -> DictNode:
    """Return sample data `dict`."""
    return msgspec.json.decode(sample_str)
