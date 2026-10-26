"""Implements `SaveData`."""

import datetime as dt
from typing import Self

import msgspec

from .params import Params


class SaveData(msgspec.Struct, kw_only=True):
    """Implements `SaveData`."""

    # key metadata
    name: str
    saveTime: dt.datetime
    map: str
    serverID: bool
    campaignID: str
    version: str
    params: Params
    factions: list[str]

    # Rebel faction
    hr: int
    resourcesFIA: int
    skillFIA: int
    randomizeRebelLoadoutUniforms: bool
    petrosPosition: Position
    unlockedVehicleTypes: list[str]
    watchpostsFIA: list[tuple[Position, list[str]]]
    roadblocksFIA: list[tuple[Position, list[str]]]
    hmgpostsFIA: list[tuple[Position, list[str]]]
    atpostsFIA: list[tuple[Position, list[str]]]
    aapostsFIA: list[tuple[Position, list[str]]]
    constructionsX: list[Position]
    # "posHQ": []
    # "rebelLoadouts": {},

    # Rival faction
    isRivalsDiscoveryQuestAssigned: bool
    areRivalsDiscovered: bool
    areRivalsDefeated: bool
    rivalsLocationsMap: dict[str, bool]
    rivalsExcludedLocations: dict[str, object]
    nextRivalsLocationReveal: float
    mrkSDK: list[str]
    controlsSDK: list[str]
    # "inactivityRivals": []

    # Occupants and Invaders
    areOccupantsDefeated: bool
    areInvadersDefeated: bool
    occupantsRadioKeys: int
    invaderRadioKeys: int
    aggressionOccupants: list[object]
    enemyResources: tuple[float, float, float, float]
    mrkCSAT: list[str]
    prestigeOPFOR: list[float]

    # Trader
    isTraderQuestCompleted: bool
    traderPosition: Position
    traderDiscount: int

    # Player state
    # "player_01234567890123456_scorePlayer": int
    # "player_01234567890123456_loadoutPlayer": []
    # "player_01234567890123456_moneyX": int
    # "player_01234567890123456_personalGarage": []
    # "player_01234567890123456_pluginsData": {},
    # "player_01234567890123456_rankPlayer": "SERGEANT",

    DLC: list[int] = []
    membersX: list[str] = []
    HQKnowledge: list[object]
    savedPlayers: list[str] = []
    A3A_fuelAmountleftArray: list[object]
    tasks: list[object]
    bombRuns: int
    wurzelGarrison: list[list[str | list[object]]]
    supportPoints: int
    antennas: list[Position]
    killZones: list[list[str | list[object]]]
    gameMode: int
    minesX: list[list[object]]
    destroyedBuildings: list[Position]
    destroyedMilAdmins: list[Position]
    destroyedSites: list[Position]
    distanceSPWN: int
    chopForest: bool
    revealedZones: list[str]
    dateX: dt.datetime

    # "HR_Garage": [],
    # "jna_dataList": [],
    # "weather": [],
    # "usesWurzelGarrison": true,
    # "staticsX": [],
    # "prestigeBLUFOR": [],
    # "aggressionInvaders": [],
    # "testingTimerIsActive": false,
    # "saveDataPlugins": {},
    # "addonVics": [],
    # "garrison": []

    @classmethod
    def decode_str(cls, json_str: str) -> SaveData:
        """Decode a JSON string into a `SaveData` object."""
        raw = msgspec.json.decode(json_str)
        raw["saveTime"] = _convert_saveTime(raw["saveTime"])
        raw["dateX"] = _convert_dateX(raw["dateX"])
        return msgspec.convert(raw, type=cls)


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


class Position(msgspec.Struct, array_like=True, forbid_unknown_fields=True):
    """Implements `Position`."""

    x: float
    y: float
    z: float = 0

    @classmethod
    def convert(cls, value: tuple[float, float] | tuple[float, float, float]) -> Self:
        """Convert an array-like of 2 or 3 `float`s to a `Position` object."""
        return msgspec.convert(value, type=cls)
