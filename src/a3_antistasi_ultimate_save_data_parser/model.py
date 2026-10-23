"""Implements `SaveData`."""

import datetime as dt
from typing import Self

import msgspec


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
    rivalsExcludedLocations: dict
    nextRivalsLocationReveal: float
    mrkSDK: list[str]
    controlsSDK: list[str]
    # "inactivityRivals": []

    # Occupants and Invaders
    areOccupantsDefeated: bool
    areInvadersDefeated: bool
    occupantsRadioKeys: int
    invaderRadioKeys: int
    aggressionOccupants: list
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
    HQKnowledge: list
    savedPlayers: list[str] = []
    A3A_fuelAmountleftArray: list
    tasks: list
    bombRuns: int
    wurzelGarrison: list[list[str | list]]
    supportPoints: int
    antennas: list[Position]
    killZones: list[list[str | list]]
    gameMode: int
    minesX: list[list]
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
        raw["saveTime"] = _convert_7_element_datetime(raw["saveTime"])
        raw["dateX"] = _convert_5_element_datetime(raw["dateX"])
        return msgspec.convert(raw, type=cls)


def _convert_5_element_datetime(value: tuple[int, int, int, int, int]) -> dt.datetime:
    """Convert an array-like of 5 `int`s to a `dt.datetime` object in UTC."""
    y, m, d, h, mn = value
    return dt.datetime(y, m, d, h, mn, tzinfo=dt.UTC)


def _convert_7_element_datetime(
    value: tuple[int, int, int, int, int, int, int],
) -> dt.datetime:
    """Convert an array-like of 7 `int`s to a `dt.datetime` object in UTC."""
    y, m, d, h, mn, s, ms = value
    return dt.datetime(y, m, d, h, mn, s, ms * 1000, tzinfo=dt.UTC)


class Position(msgspec.Struct, array_like=True, forbid_unknown_fields=True):
    """Implements `Position`."""

    x: float
    y: float
    z: float = 0

    @classmethod
    def convert(cls, value: tuple[float, float] | tuple[float, float, float]) -> Self:
        """Convert an array-like of 2 or 3 `float`s to a `Position` object."""
        return msgspec.convert(value, type=cls)


class Params(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Implements `Param`."""

    A3A_attackHQProximityMul: int
    A3A_builderAllowRoads: bool
    A3A_builderBuildTime: int
    A3A_builderLimit: int
    A3A_builderPermissions: int
    A3A_diameterExtendedCaptureArea: int
    A3A_enemyAttackMul: int
    A3A_enemyBalanceMul: int
    A3A_enemyResponseTime: int
    A3A_enemySkillMul: int
    A3A_flagGarageBlock: int
    A3A_GCThreshold: int
    A3A_guestCommander: bool
    A3A_guestItemLimit: int
    A3A_idleTimeout: int
    A3A_invaderBalanceMul: int
    A3A_isUAVAFK: bool
    A3A_isZeusAFK: bool
    A3A_logDebugConsole: int
    A3A_rebelGarrisonGroupSize: int
    A3A_rebelGarrisonLimit: int
    A3A_rebelSkillMul: int
    A3A_removeRestore: bool
    A3A_reviveTime: int
    A3A_roadBlocksBaseChance: int
    A3A_selfReviveMethods: bool
    A3A_showGroupBar: bool
    A3A_UAVSpawnChance: int
    A3A_ultimate_allowLockpickKits: bool
    A3A_ultimate_lockpickKitBreakChance: int
    A3A_ultimate_trader_selling_sellPriceMultiplier: int
    A3U_blackMarketDiscountVehicle: int
    A3U_blackMarketDiscountWeapon: int
    A3U_disableMortars: bool
    A3U_disablePATCOMMortars: bool
    A3U_enableVehiclesForAI: bool
    A3U_HelipadTerrainSmoothing: bool
    aceFood: bool
    aiAccuracyCeiling: int
    AIBalanceParams: int
    AIBalanceParamsSpacer: int
    aiControlTime: int
    AIParams: int
    AIParamsSpacer2: int
    AIParamsSpacer: int
    AIrevivesOutsideSquad: int
    allowCivDialog: bool
    allowFuturisticSupports: bool
    allowFuturisticUnfairSupports: bool
    allowGuidedLaunchers: int
    allowUnfairSupports: bool
    allowUnlockedExplosives: int
    allowUnlockedTNVG: int
    AllParams: int
    areRandomEventsEnabled: bool
    areRivalsEnabled: bool
    autoSave: bool
    autoSaveInterval: int
    BalanceParamsSpacer: int
    BasicParams: int
    BasicParamsSpacer: int
    blackMarketIgnoreRequirements: bool
    BMParams: int
    BMParamsSpacer2: int
    BMParamsSpacer: int
    BuilderParams: int
    BuilderParamsSpacer: int
    civTraffic: int
    cosmeticsEnabled: bool
    crateAmmoNumMax: int
    crateAmmoTypeMax: int
    crateAttachmentNumMax: int
    crateAttachmentTypeMax: int
    crateBackpackNumMax: int
    crateBackpackTypeMax: int
    crateDeviceNumMax: int
    crateDeviceTypeMax: int
    crateExplosiveNumMax: int
    crateExplosiveTypeMax: int
    crateHelmetNumMax: int
    crateHelmetTypeMax: int
    crateItemNumMax: int
    crateItemTypeMax: int
    CrateParams: int
    CrateParamsSpacer: int
    crateVestNumMax: int
    crateVestTypeMax: int
    crateWepNumMax: int
    crateWepTypeMax: int
    createAmbientSounds: bool
    deathPenalty: int
    DevelopmentParams: int
    DevelopmentParamsSpacer: int
    disableTrader: bool
    distanceMission: int
    distanceSPWN: int
    enablePunishments: int
    enableSpectrumDevice: bool
    enableVehicleAutoLock: bool
    enableVehicleAutoLockCiv: bool
    enemyNearDistance: int
    ExperimentalParams: int
    ExperimentalParamsSpacer: int
    ExtenderParams: int
    ExtenderParamsSpacer: int
    fastTravelEnemyCheck: bool
    fatigueEnabled: bool
    gameMode: int
    globalCivilianMax: int
    helmetLossChance: int
    helmetLossSound: bool
    hideEnemyMarkers: bool
    hideEnemyMarkersReconPlaneDistance: int
    initialFactionMoney: int
    initialHr: int
    initialPlayerMoney: int
    limitHR: int
    limitWeaponsByUnitType: bool
    limitedFT: int
    loadoutArsenalDefaultOverride: bool
    loadoutsToGenerate: int
    LogLevel: int
    lootCrateDistance: int
    lootCratePrice: int
    lootCrateUnlockedItems: bool
    lootCratesEnabled: bool
    LootParams: int
    loseHROnDeath: int
    lossCondition: int
    magRepack: bool
    maxCiviliansPerTown: int
    maxConstructions: int
    maxSupportPoints: int
    MemberParams: int
    MemberParamsSpacer: int
    membershipEnabled: bool
    minWeaps: int
    MiscBalanceParams: int
    MiscBalanceParamsSpacer: int
    MiscLootParams: int
    MiscLootParamsSpacer: int
    napalmEnabled: bool
    newCarTowing: bool
    overallHRGain: int
    pistolStart: bool
    playerIcons: bool
    playerMarkersEnabled: bool
    playerRecruitAI: int
    plusGarrison: bool
    radiomanSupport: bool
    rallyPointSpawnCount: int
    RebelBalanceParams: int
    recruitToPlayerSquad: bool
    reviveKitsEnabled: bool
    rivalsDifficulty: int
    RRTurretMagazines: bool
    saveZeusBuildings: bool
    ScenarioParams: int
    ScriptParams: int
    ScriptParamsSpacer: int
    settingsTimeMultiplier: int
    staminaEnabled: bool
    startWithLongRangeRadio: bool
    swayEnabled: int
    TimerParams: int
    TimerParamsSpacer: int
    tkPunish: bool
    townSkirmishChance: int
    unconChanceEny: int
    unconChanceReb: int
    unconsciousPossessAi: bool
    unflipPersonCount: int
    unlockedUnlimitedAmmo: int
    UnlockParams: int
    useDownedNotification: bool
    vanillaArmsDealer: bool
    vehicleLockpickTime: int
    VehicleLootParams: int
    VehicleLootParamsSpacer: int
    victoryCondition: int
    zombiesUncapped: bool
