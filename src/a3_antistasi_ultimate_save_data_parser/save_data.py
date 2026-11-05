"""Implements `SaveData`."""

import datetime as dt
import importlib.metadata
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, ClassVar, Literal
from uuid import UUID

import msgspec

from .params import Params
from .player_data import PlayerData
from .position import Position, Position2D
from .types import SteamId64

if TYPE_CHECKING:
    from collections.abc import Iterable

_PACKAGE_VERSION = importlib.metadata.version("a3_antistasi_ultimate_save_data_parser")


type _RawPosition = Sequence[float]


class SaveData(msgspec.Struct, kw_only=True):
    """Provides an interface for Antistasi Ultimate JSON save data.

    All field names correspond to source JSON keys (unless noted),
    so don't conform to conventional Python 'PEP8' naming patterns.

    Descriptors: https://github.com/Antistasi-Ultimate-Community/A3-Antistasi-Ultimate/blob/unstable/A3A/addons/core/functions/init/fn_initServer.sqf
    """

    __DERIVED_FIELDS__: ClassVar[set[str]] = {
        "__a3_antistasi_ultimate_save_data_parser_version__",
        "players",
    }
    """@public Fields that are derived during parsing, so will never be in input."""

    __a3_antistasi_ultimate_save_data_parser_version__: str
    """@public The version of this library used to parse the JSON data.

    Does not correspond to a source JSON key.
    """

    # Key metadata:
    name: str  # including empty ""
    saveTime: dt.datetime
    """UTC timestamp of the save. Millisecond precision."""
    serverID: str | Literal[False]
    campaignID: UUID
    version: str
    params: Params
    """Mission parameters as a `.params.Params` instance."""
    factions: list[str]
    membersX: list[SteamId64]
    """`list` of `.types.SteamId64`s."""
    savedPlayers: list[SteamId64]
    """`list` of `.types.SteamId64`s."""
    players: dict[SteamId64, PlayerData] = {}
    """`dict` mapping `.types.SteamId64` to `.player_data.PlayerData` instances.

    Does not correspond directly to a source JSON key.
    """

    # World:
    map: str  # e.g. "Altis"
    dateX: dt.datetime
    """Geographic time within the mission with minutes precision. No timezone."""
    weather: list[object]

    # Rebel faction:
    hr: int
    resourcesFIA: int
    skillFIA: int
    randomizeRebelLoadoutUniforms: bool
    petrosPosition: Position
    unlockedVehicleTypes: list[str]  # e.g. ["Unarmed Cars", "Armed Cars"]
    posHQ: list[tuple[float, Any] | Any]
    """Actual type is `list[tuple[float, .position.Position] | .position.Position]`."""
    # msgspec doesn't allow more complex type union expressions
    # e.g. can't use more than one array-like, such as _RawPosition/list/tuple
    # this forces parsing to positions later
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
    traderPosition: Position2D | None
    traderDiscount: int

    # Other / TODO:
    DLC: list[int] = []
    HQKnowledge: list[object]  # observed pattern: [float, float, [], []]
    A3A_fuelAmountleftArray: list[tuple[Position, float]]
    # observed patterns:
    # []
    # [[Position, 1] ...]
    tasks: list[object]
    bombRuns: int
    wurzelGarrison: list[list[str | list[object]]]
    """Where `str` is a marker name e.g. `'outpost_49'`
    or town name, e.g. `'Agios Dionysios'`."""
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
        raw.update(
            {
                "__a3_antistasi_ultimate_save_data_parser_version__": _PACKAGE_VERSION,
                "saveTime": _convert_saveTime(raw["saveTime"]),
                "dateX": _convert_dateX(raw["dateX"]),
                "membersX": _convert_iterable_str_to_int(raw["membersX"]),
                "savedPlayers": _convert_iterable_str_to_int(raw["savedPlayers"]),
                "traderPosition": _convert_traderPosition(raw["traderPosition"]),
                "posHQ": _convert_posHQ(raw["posHQ"]),
                "players": PlayerData._dict_from_raw_dict(raw),
                "params": Params._from_dict(raw["params"]),
            },
        )
        return msgspec.convert(raw, type=cls)  # this does re-validate some data


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


def _convert_traderPosition(value: Sequence[float]) -> Position2D | None:
    if not value:
        return None

    if _is_raw_position2D(value):
        return Position2D._from_raw_position_array(value)

    err_msg = (
        f"Can't convert `traderPosition` value: "
        f"'{value}' of type '{type(value)}'. "
        f"Expected `{_RawPosition}`."
    )
    raise TypeError(err_msg)


def _convert_posHQ(
    value: Iterable[tuple],
) -> list[tuple[float, Position] | Position]:
    output: list[tuple[float, Position] | Position] = []
    for item in value:
        if _is_raw_position(item):
            output.append(Position._from_raw_position_array(item))

        elif (
            isinstance(item, Sequence)
            and isinstance(item[0], float)
            and _is_raw_position(item[1])
        ):
            output.append((item[0], Position._from_raw_position_array(item[1])))

        else:
            err_msg = (
                f"Can't convert `posHQ` array item: "
                f"'{item}' of type '{type(item)}'. "
                f"Expected `{_RawPosition}` or `tuple[float, _RawPosition]`."
            )
            raise TypeError(err_msg)

    return output


def _convert_iterable_str_to_int(value: Iterable[str]) -> list[int]:
    """Convert an iterable of `str`s to list of `int`s`."""
    return [int(x) for x in value]


def _is_raw_position(value: object) -> bool:
    return (
        isinstance(value, Sequence)
        and len(value) == 3  # noqa: PLR2004
        and all(isinstance(x, float | int) for x in value)
    )


def _is_raw_position2D(value: object) -> bool:
    return (
        isinstance(value, Sequence)
        and len(value) == 2  # noqa: PLR2004
        and all(isinstance(x, float | int) for x in value)
    )
