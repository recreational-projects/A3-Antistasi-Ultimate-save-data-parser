"""Implements `Position`."""

import msgspec


class Position(msgspec.Struct, array_like=True, forbid_unknown_fields=True):
    """A 3D position in the world.

    See also https://community.bistudio.com/wiki/Position

    Source JSON doesn't identify variants with differing datums
    like PositionASL, Position ATL, PositionAGL.
    """

    x: float
    y: float
    z: float = 0
    """Height/altitude relative to a datum."""
