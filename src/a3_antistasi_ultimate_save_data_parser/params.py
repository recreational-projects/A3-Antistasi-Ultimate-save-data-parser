"""Implements `Params`.

All field names correspond to source JSON keys (unless noted),
so don't conform to conventional Python 'PEP8' naming patterns.
"""

from typing import TYPE_CHECKING, ClassVar, Self

import msgspec

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode


class Params(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Mission parameters.

    Ref: https://github.com/Antistasi-Ultimate-Community/A3-Antistasi-Ultimate/blob/unstable/A3A/addons/core/Params.hpp
    """

    _DISCARD_KEYS: ClassVar[set[str]] = {
        "AllParams",
        # basic:
        "BasicParams",
        "BasicParamsSpacer",
        "ScenarioParams",
        "MemberParams",
        "MemberParamsSpacer",
        "ScriptParams",
        "ScriptParamsSpacer",
        "TimerParams",
        "TimerParamsSpacer",
        # ai and balance:
        "AIParams",
        "AIParamsSpacer",
        "AIParamsSpacer2",
        "BalanceParamsSpacer",
        "RebelBalanceParams",
        "AIBalanceParamsSpacer",
        "AIBalanceParams",
        "MiscBalanceParamsSpacer",
        "MiscBalanceParams",
        # bm:
        "BMParams",
        "BMParamsSpacer",
        "BMParamsSpacer2",
        # builder:
        "BuilderParams",
        "BuilderParamsSpacer",
        # loot:
        "LootParams",
        "CrateParams",
        "CrateParamsSpacer",
        "VehicleLootParams",
        "VehicleLootParamsSpacer",
        "MiscLootParams",
        "MiscLootParamsSpacer",
        # extender:
        "ExtenderParams",
        "ExtenderParamsSpacer",
        "YourExtenderNameSpacer",
        "YourExtenderNameParams",
        # experimental:
        "ExperimentalParams",
        "ExperimentalParamsSpacer",
        # development:
        "DevelopmentParams",
        "DevelopmentParamsSpacer",
        # deprecated:
        "DeprecatedParams",
        "DeprecatedParamsSpacer",
        # removed:
        "A3A_showGroupBar",
        # Removed in A3U 12.3.0.0.
        # May appear in new exports made from A3U 12.2.0.0 saves
    }

    basic: BasicParams
    """Contains Basic mission parameters as a `BasicParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    ai: AIParams
    """Contains AI and Balance mission parameters as an `AIParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    bm: BMParams
    """Contains BlackMarket mission parameters as a `BMParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    builder: BuilderParams
    """Contains Builder mission parameters as a `BuilderParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    loot: LootParams
    """Contains Loot mission parameters as a `LootParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    extender: ExtenderParams
    """Contains Extender mission parameters as an `ExtenderParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    experimental: ExperimentalParams
    """Contains Experimental mission parameters as an `ExperimentalParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    deprecated: DeprecatedParams
    """Contains Deprecated mission parameters as a `DeprecatedParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    development: DevelopmentParams
    """Contains Development mission parameters as a `DevelopmentParams` instance.

    Doesn't directly correspond to a source JSON key,
    but reflects AU source code structure.
    """
    A3A_flagGarageBlock: int
    # A3A_showGroupBar: bool  # removed in AU 12.3.0.0

    @classmethod
    def _from_dict(cls, dict_: JSONDictNode) -> Self:
        """Construct a type-validated instance from a `dict` JSON conversion."""
        sub_params: dict[str, _SubParams] = {}
        consumed_keys: set[str] = set()
        for param_field_name, sub_param_type in cls._get_sub_params_types().items():
            _sub_param_data = {
                f: dict_.get(f) for f in sub_param_type.__struct_fields__
            }
            sub_params[param_field_name] = msgspec.convert(
                _sub_param_data, sub_param_type
            )
            consumed_keys |= _sub_param_data.keys()

        remaining_data = {
            k: dict_[k] for k in dict_ if k not in consumed_keys | cls._DISCARD_KEYS
        }
        return msgspec.convert({**remaining_data, **sub_params}, type=cls)

    @classmethod
    def _get_sub_params_types(cls) -> dict[str, type[_SubParams]]:
        """Get a `dict` mapping sub parameter names to types, via introspection."""
        return {
            m.name: m.type
            for m in msgspec.structs.fields(cls)
            if issubclass(m.type, _SubParams)
        }


class _SubParams(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Sub mission parameters."""


class BasicParams(_SubParams):
    """Basic mission parameters."""

    ### ScenarioParams
    gameMode: int
    areRivalsEnabled: bool
    rivalsDifficulty: int
    victoryCondition: int
    lossCondition: int
    areRandomEventsEnabled: bool
    createAmbientSounds: bool

    ### MemberParams
    membershipEnabled: bool
    A3A_guestCommander: bool
    tkPunish: bool

    ### ScriptParams
    magRepack: bool
    RRTurretMagazines: bool
    newCarTowing: bool

    ### TimerParams
    autoSave: bool
    autoSaveInterval: int
    A3A_idleTimeout: int
    A3A_isUAVAFK: bool
    A3A_isZeusAFK: bool
    A3A_GCThreshold: int
    settingsTimeMultiplier: int


class AIParams(_SubParams):
    """AI and Balance mission parameters."""

    distanceSPWN: int
    enemyNearDistance: int
    A3A_roadBlocksBaseChance: int
    globalCivilianMax: int
    maxCiviliansPerTown: int
    civTraffic: int
    allowCivDialog: bool
    zombiesUncapped: bool
    plusGarrison: bool
    radiomanSupport: bool
    playerRecruitAI: int
    recruitToPlayerSquad: bool
    aiControlTime: int
    unconsciousPossessAi: bool
    loadoutsToGenerate: int
    AIrevivesOutsideSquad: int

    # RebelBalanceParams
    initialPlayerMoney: int
    initialFactionMoney: int
    deathPenalty: int
    initialHr: int
    limitHR: int
    overallHRGain: int
    loseHROnDeath: int
    maxSupportPoints: int
    pistolStart: bool
    startWithLongRangeRadio: bool
    aceFood: bool
    enableSpectrumDevice: bool
    reviveKitsEnabled: bool
    A3A_reviveTime: int
    A3A_selfReviveMethods: bool
    useDownedNotification: bool
    rallyPointSpawnCount: int
    staminaEnabled: bool
    fatigueEnabled: bool
    swayEnabled: int
    A3A_removeRestore: bool
    limitedFT: int
    fastTravelEnemyCheck: bool
    unflipPersonCount: int
    A3A_rebelGarrisonLimit: int
    A3A_rebelGarrisonGroupSize: int

    # AIBalanceParams
    A3A_enemyBalanceMul: int
    A3A_enemyAttackMul: int
    A3A_invaderBalanceMul: int
    enablePunishments: int
    townSkirmishChance: int
    A3A_enemyResponseTime: int
    A3A_attackHQProximityMul: int
    A3A_enemySkillMul: int
    A3A_rebelSkillMul: int
    aiAccuracyCeiling: int
    unconChanceEny: int
    unconChanceReb: int
    napalmEnabled: bool
    allowUnfairSupports: bool
    allowFuturisticSupports: bool
    allowFuturisticUnfairSupports: bool
    A3U_disablePATCOMMortars: bool
    A3U_disableMortars: bool
    A3A_UAVSpawnChance: int
    distanceMission: int
    A3U_enableVehiclesForAI: bool

    # MiscBalanceParams
    playerMarkersEnabled: bool
    hideEnemyMarkers: bool
    hideEnemyMarkersReconPlaneDistance: int
    playerIcons: bool
    loadoutArsenalDefaultOverride: bool
    limitWeaponsByUnitType: bool
    A3A_diameterExtendedCaptureArea: int
    A3A_ultimate_allowLockpickKits: bool
    A3A_ultimate_lockpickKitBreakChance: int


class BMParams(_SubParams):
    """BlackMarket mission parameters."""

    disableTrader: bool
    A3A_ultimate_trader_selling_sellPriceMultiplier: int
    vanillaArmsDealer: bool
    blackMarketIgnoreRequirements: bool
    A3U_blackMarketDiscountVehicle: int
    A3U_blackMarketDiscountWeapon: int


class BuilderParams(_SubParams):
    """Builder mission parameters."""

    A3A_builderPermissions: int
    A3A_builderLimit: int
    A3A_builderBuildTime: int
    A3A_builderAllowRoads: bool
    A3U_HelipadTerrainSmoothing: bool
    saveZeusBuildings: bool
    maxConstructions: int


class LootParams(_SubParams):
    """Loot mission parameters."""

    ### UnlockParams
    UnlockParams: int
    minWeaps: int
    A3A_guestItemLimit: int
    unlockedUnlimitedAmmo: int
    allowGuidedLaunchers: int
    allowUnlockedExplosives: int
    allowUnlockedTNVG: int
    cosmeticsEnabled: bool

    ### CrateParams
    lootCratesEnabled: bool
    lootCrateDistance: int
    lootCratePrice: int
    lootCrateUnlockedItems: bool
    crateWepTypeMax: int
    crateWepNumMax: int
    crateItemTypeMax: int
    crateItemNumMax: int
    crateAmmoTypeMax: int
    crateAmmoNumMax: int
    crateExplosiveTypeMax: int
    crateExplosiveNumMax: int
    crateAttachmentTypeMax: int
    crateAttachmentNumMax: int
    crateBackpackTypeMax: int
    crateBackpackNumMax: int
    crateVestTypeMax: int
    crateVestNumMax: int
    crateHelmetTypeMax: int
    crateHelmetNumMax: int
    crateDeviceTypeMax: int
    crateDeviceNumMax: int

    ### VehicleLootParams
    enableVehicleAutoLock: bool
    enableVehicleAutoLockCiv: bool
    vehicleLockpickTime: int

    ### MiscLootParams
    helmetLossChance: int
    helmetLossSound: bool


class ExtenderParams(_SubParams):
    """Extender mission parameters."""

    A3UE_YourExtenderName_ParamName: object | None = None
    # not sure where this presumably placeholder field
    # comes from. Added in AU 12.3.0.0, or is it from an extender?


class ExperimentalParams(_SubParams):
    """Experimental mission parameters."""


class DevelopmentParams(_SubParams):
    """Development mission parameters."""

    LogLevel: int
    A3A_logDebugConsole: int


class DeprecatedParams(_SubParams):
    """Deprecated mission parameters."""
