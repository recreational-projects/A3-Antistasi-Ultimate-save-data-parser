"""Implements `Position`."""

import msgspec


class Position(msgspec.Struct, array_like=True, forbid_unknown_fields=True):
    """Implements `Position`."""

    x: float
    y: float
    z: float = 0
