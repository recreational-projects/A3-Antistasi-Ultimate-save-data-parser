"""Simple types for internal use."""

import math
from typing import Any, NewType, TypeIs

type SteamId64 = int
"""Validated to be 17 digit `int`."""

_LEN_STEAM_ID64 = 17


def _is_steam_id_64(value: int) -> TypeIs[SteamId64]:
    return isinstance(value, int) and int(math.log10(value)) + 1 == _LEN_STEAM_ID64


_JSONDictNode = NewType("_JSONDictNode", dict[str, Any])
"""For type checking, effectively a subtype of `dict[str, Any]` """
