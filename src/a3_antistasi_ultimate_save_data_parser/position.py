"""Implements position classes."""

from typing import TYPE_CHECKING, Self

import msgspec

if TYPE_CHECKING:
    from collections.abc import Sequence


class Position(
    msgspec.Struct, array_like=True, forbid_unknown_fields=True, kw_only=True
):
    """A 3D position in the world.

    See also https://community.bistudio.com/wiki/Position

    Source JSON doesn't identify variants with differing datums
    like PositionASL, Position ATL, PositionAGL.
    """

    x: float
    y: float
    z: float
    """Height/altitude relative to a datum."""

    @classmethod
    def _from_raw_position_array(cls, value: Sequence[float | int]) -> Self:
        return cls(x=value[0], y=value[1], z=value[2])


class Position2D(
    msgspec.Struct, array_like=True, forbid_unknown_fields=True, kw_only=True
):
    """A 2D position in the world.

    See also https://community.bistudio.com/wiki/Position
    """

    x: float
    y: float

    @classmethod
    def _from_raw_position_array(cls, value: Sequence[float | int]) -> Self:
        return cls(x=value[0], y=value[1])
