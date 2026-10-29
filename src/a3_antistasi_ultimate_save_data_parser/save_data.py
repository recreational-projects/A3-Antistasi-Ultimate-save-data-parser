"""Implements `SaveData`."""

import datetime as dt
import importlib.metadata
from typing import TYPE_CHECKING, ClassVar

import msgspec

from ._types import SteamId64
from .params import Params
from .player_data import PlayerData
from .position import Position

if TYPE_CHECKING:
    from collections.abc import Iterable


class SaveData(msgspec.Struct, kw_only=True):
    """Provides an interface for Antistasi Ultimate JSON save data."""

    DERIVED_FIELDS: ClassVar[set[str]] = {
        "__a3_antistasi_ultimate_save_data_parser_version__",
        "players",
    }
    """Fields that are derived during parsing, so will never be in input."""

    __a3_antistasi_ultimate_save_data_parser_version__: str
    """@public The version of this library used to parse the JSON data."""

    # Key metadata:
    name: str  # including empty ""
    saveTime: dt.datetime
    """UTC timestamp of the save."""
    serverID: bool
    campaignID: str
    version: str
    params: Params
    """Mission parameters as a `.params.Params` instance."""
    factions: list[str]
    membersX: list[SteamId64]
    """`list` of `SteamId64`s."""
    savedPlayers: list[SteamId64]
    """`list` of `SteamId64`s."""
    players: dict[SteamId64, PlayerData] = {}
    """`dict` mapping `SteamId64` to `.player.PlayerData` instances."""

    # World:
    map: str  # e.g. "Altis"
    dateX: dt.datetime
    """Geographic time within the mission; no timezone."""
    weather: list[object]

    # Rebel faction:
    hr: int
    resourcesFIA: int
    skillFIA: int
    randomizeRebelLoadoutUniforms: bool
    petrosPosition: Position
    unlockedVehicleTypes: list[str]  # e.g. ["Unarmed Cars", "Armed Cars"]
    posHQ: list[object]
    watchpostsFIA: list[tuple[Position, list[str]]]  # including empty []
    roadblocksFIA: list[tuple[Position, list[str]]]  # including empty []
    hmgpostsFIA: list[tuple[Position, list[str]]]  # including empty []
    atpostsFIA: list[tuple[Position, list[str]]]  # including empty []
    aapostsFIA: list[tuple[Position, list[str]]]  # including empty []
    constructionsX: list[Position]  # including empty []
    rebelLoadouts: dict[str, object]  # including empty {}

    # Rival faction:
    isRivalsDiscoveryQuestAssigned: bool
    areRivalsDiscovered: bool
    areRivalsDefeated: bool
    rivalsLocationsMap: dict[str, bool]  # Town names
    rivalsExcludedLocations: dict[str, object]  # including empty {}
    nextRivalsLocationReveal: float
    mrkSDK: list[str]  # marker names inc. "SyndHQ"
    controlsSDK: list[str]  # marker names
    inactivityRivals: tuple[int, list[list[float]]]

    # Occupants and Invaders:
    areOccupantsDefeated: bool
    areInvadersDefeated: bool
    occupantsRadioKeys: int
    invaderRadioKeys: int
    aggressionOccupants: list[object]  # observed patterns:  [1,[]]
    enemyResources: tuple[float, float, float, float]
    mrkCSAT: list[str]  # marker names
    prestigeOPFOR: list[float]  # variable length

    # Trader:
    isTraderQuestCompleted: bool
    traderPosition: Position | None
    traderDiscount: int

    # Other / TODO:
    DLC: list[int] = []
    HQKnowledge: list[object]  # observed pattern: [float, float, [], []]
    A3A_fuelAmountleftArray: list[object]
    # observed patterns:
    # []
    # [[Position], 1 ...]
    tasks: list[object]
    bombRuns: int
    wurzelGarrison: list[list[str | list[object]]]
    supportPoints: int
    antennas: list[Position]  # including empty []
    killZones: list[list[str | list[object]]]
    gameMode: int
    minesX: list[list[object]]
    destroyedBuildings: list[Position]  # including empty []
    destroyedMilAdmins: list[Position]  # including empty []
    destroyedSites: list[Position]
    distanceSPWN: int
    chopForest: bool
    revealedZones: list[str]
    HR_Garage: list[object]
    jna_dataList: list[list[object]]
    usesWurzelGarrison: bool
    staticsX: list[list[object]]
    prestigeBLUFOR: list[float]
    aggressionInvaders: list[object]
    testingTimerIsActive: bool
    saveDataPlugins: dict[object, object]
    addonVics: list[object]
    garrison: list[list[object]]

    @classmethod
    def decode_str(cls, json_str: str) -> SaveData:
        """Decode a JSON string into a `SaveData` instance."""
        raw = msgspec.json.decode(json_str)  # naive conversion to Python builtins

        # in-place conversions to builtins / external types:
        raw["saveTime"] = _convert_saveTime(raw["saveTime"])
        raw["dateX"] = _convert_dateX(raw["dateX"])
        raw["membersX"] = _convert_iterable_str_to_int(raw["membersX"])
        raw["savedPlayers"] = _convert_iterable_str_to_int(raw["savedPlayers"])
        raw["traderPosition"] = _convert_traderPosition(raw["traderPosition"])

        _pkg_version = importlib.metadata.version(
            "a3_antistasi_ultimate_save_data_parser"
        )
        _player_dict = PlayerData._dict_from_raw_dict(raw)  # noqa: SLF001
        additional_fields = {
            "__a3_antistasi_ultimate_save_data_parser_version__": _pkg_version,
            "players": _player_dict,
        }
        return msgspec.convert(
            {
                **raw,
                **additional_fields,
            },
            type=cls,
        )


def _convert_saveTime(
    value: tuple[int, int, int, int, int, int, int],
) -> dt.datetime:
    """Convert `saveTime` field value."""
    y, m, d, h, mn, s, ms = value
    return dt.datetime(y, m, d, h, mn, s, ms * 1000, tzinfo=dt.UTC)


def _convert_dateX(value: tuple[int, int, int, int, int]) -> dt.datetime:
    """Convert `dateX` field value. Resulting datetime is not in a timezone."""
    y, m, d, h, mn = value
    return dt.datetime(y, m, d, h, mn, tzinfo=None)


def _convert_traderPosition(value: Iterable[float]) -> Position | None:
    if not value:
        return None

    return Position(*value)


def _convert_iterable_str_to_int(value: Iterable[str]) -> list[int]:
    """Convert an iterable of `str`s to list of `int`s`."""
    return [int(x) for x in value]
