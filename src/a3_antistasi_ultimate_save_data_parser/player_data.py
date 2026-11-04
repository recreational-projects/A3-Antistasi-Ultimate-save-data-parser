"""Implements `PlayerData`."""

from typing import TYPE_CHECKING, Any, Self

import msgspec

from a3_antistasi_ultimate_save_data_parser.types import _is_steam_id_64

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser.types import SteamId64

_SOURCE_PLAYER_FIELDS_PREFIX = "player_"


class PlayerData(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Data for a player.

    All field names correspond to source JSON keys,
    so don't conform to conventional Python 'PEP8' naming patterns.
    """

    scorePlayer: int
    loadoutPlayer: list[object]
    moneyX: int
    personalGarage: list[object]
    pluginsData: dict[str, object]
    rankPlayer: str

    @classmethod
    def _dict_from_raw_dict(cls, raw_dict: dict[str, Any]) -> dict[SteamId64, Self]:
        """Derive `dict` of `STEAM_ID`: `PlayerData()`.

        from e.g. the initial conversion of save data JSON to `dict` of Python builtins,
        which contains keys like 'player_STEAM_ID_scorePlayer'.
        """
        steam_ids = {
            _steam_id_64_from_player_data_key(key)
            for key in raw_dict
            if key.startswith(_SOURCE_PLAYER_FIELDS_PREFIX)
        }
        return {
            steam_id: cls._from_raw_dict(raw_dict=raw_dict, steam_id=steam_id)
            for steam_id in steam_ids
        }

    @classmethod
    def _from_raw_dict(cls, *, raw_dict: dict[str, Any], steam_id: SteamId64) -> Self:
        """Construct a type-validated instance.

        from e.g. the initial conversion of save data JSON to `dict` of Python builtins,
        which contains keys like 'player_STEAM_ID_scorePlayer'.
        """
        field_names = {f.name for f in msgspec.structs.fields(cls)}
        player_data = {
            field_name: raw_dict[
                f"{_SOURCE_PLAYER_FIELDS_PREFIX}{steam_id}_{field_name}"
            ]
            for field_name in field_names
        }
        return msgspec.convert(player_data, type=cls)


def _steam_id_64_from_player_data_key(key: str) -> int:
    """Return a `SteamID64` from a source data key. Key must start with 'player_'."""
    if not key.startswith(_SOURCE_PLAYER_FIELDS_PREFIX):
        err_msg = (
            f"Invalid key '{key}': doesn't start with '{_SOURCE_PLAYER_FIELDS_PREFIX}'"
        )
        raise TypeError(err_msg)

    steam_id = int(
        key.removeprefix(_SOURCE_PLAYER_FIELDS_PREFIX).split("_", maxsplit=1)[0]
    )
    if not _is_steam_id_64(steam_id):
        err_msg = f"Invalid Steam ID: {steam_id}"
        raise TypeError(err_msg)

    return steam_id
