"""Implements `Player`."""

from typing import TYPE_CHECKING, Any, Self

import msgspec

from a3_antistasi_ultimate_save_data_parser._types import LEN_STEAM_ID64

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import SteamId64

_PLAYER_FIELDS_PREFIX = "player_"


class Player(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Implements `Player`."""

    scorePlayer: int
    loadoutPlayer: list[object]
    moneyX: int
    personalGarage: list[object]
    pluginsData: dict[str, object]
    rankPlayer: str

    @classmethod
    def dict_from_raw_dict(cls, raw_dict: dict[str, Any]) -> dict[SteamId64, Self]:
        """Derive `dict` of `STEAM_ID`: `Player()`.

        from e.g. the initial conversion of savedata to Python builtins,
        which contains keys like 'player_STEAM_ID_scorePlayer'.
        """
        steam_ids = {
            int(k.removeprefix("player_")[:LEN_STEAM_ID64])
            for k in raw_dict
            if k.startswith(_PLAYER_FIELDS_PREFIX)
        }
        field_names = {f.name for f in msgspec.structs.fields(cls)}
        output_dict: dict[SteamId64, Self] = {}
        for steam_id in steam_ids:
            player = cls(
                **{
                    field_name: raw_dict[
                        f"{_PLAYER_FIELDS_PREFIX}{steam_id}_{field_name}"
                    ]
                    for field_name in field_names
                }
            )
            output_dict[steam_id] = player

        return output_dict
