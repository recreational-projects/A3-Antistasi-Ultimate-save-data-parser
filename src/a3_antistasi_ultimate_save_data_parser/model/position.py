"""Implements `Position`."""

from typing import Self

import msgspec


class Position(msgspec.Struct, array_like=True, forbid_unknown_fields=True):
    """Implements `Position`."""

    x: float
    y: float
    z: float = 0

    @classmethod
    def convert(cls, value: list[float]) -> Self:
        """Convert an array-like of 2 or 3 `float`s to a `Position` object."""
        return msgspec.convert(value, type=cls)
