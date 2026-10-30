"""Implements `Params`."""

import msgspec


class Params(msgspec.Struct, kw_only=True, forbid_unknown_fields=True):
    """Mission parameters.

    All field names correspond to source JSON keys (unless noted),
    so don't conform to conventional Python 'PEP8' naming patterns.
    """

    # AllParams

    AllParams: int

    ## BasicParams
    BasicParams: int

    ### ScenarioParams
    ScenarioParams: int
    gameMode: int
    areRivalsEnabled: bool
    rivalsDifficulty: int
    victoryCondition: int
    lossCondition: int
    areRandomEventsEnabled: bool
    createAmbientSounds: bool

    ### MemberParams
    MemberParamsSpacer: int
    MemberParams: int
    membershipEnabled: bool
    A3A_guestCommander: bool
    tkPunish: bool

    ### ScriptParams
    ScriptParamsSpacer: int
    ScriptParams: int
    magRepack: bool
    RRTurretMagazines: bool
    newCarTowing: bool

    ### TimerParams
    TimerParamsSpacer: int
    TimerParams: int
    autoSave: bool
    autoSaveInterval: int
    A3A_idleTimeout: int
    A3A_isUAVAFK: bool
    A3A_isZeusAFK: bool
    A3A_GCThreshold: int
    settingsTimeMultiplier: int

    BasicParamsSpacer: int

    # AIParams
    AIParamsSpacer: int
    AIParams: int
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
    BalanceParamsSpacer: int
    RebelBalanceParams: int
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
    AIBalanceParamsSpacer: int
    AIBalanceParams: int
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
    MiscBalanceParamsSpacer: int
    MiscBalanceParams: int
    playerMarkersEnabled: bool
    hideEnemyMarkers: bool
    hideEnemyMarkersReconPlaneDistance: int
    playerIcons: bool
    loadoutArsenalDefaultOverride: bool
    limitWeaponsByUnitType: bool
    A3A_diameterExtendedCaptureArea: int
    A3A_ultimate_allowLockpickKits: bool
    A3A_ultimate_lockpickKitBreakChance: int

    AIParamsSpacer2: int

    ## BMParams
    BMParamsSpacer: int
    BMParams: int

    ### LootParams
    LootParams: int
    disableTrader: bool
    A3A_ultimate_trader_selling_sellPriceMultiplier: int
    vanillaArmsDealer: bool
    blackMarketIgnoreRequirements: bool
    A3U_blackMarketDiscountVehicle: int
    A3U_blackMarketDiscountWeapon: int

    ## BuilderParams
    BuilderParamsSpacer: int
    BuilderParams: int
    A3A_builderPermissions: int
    A3A_builderLimit: int
    A3A_builderBuildTime: int
    A3A_builderAllowRoads: bool
    A3U_HelipadTerrainSmoothing: bool
    saveZeusBuildings: bool
    maxConstructions: int

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
    CrateParams: int
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
    CrateParamsSpacer: int

    ### VehicleLootParams
    VehicleLootParams: int
    enableVehicleAutoLock: bool
    enableVehicleAutoLockCiv: bool
    vehicleLockpickTime: int
    VehicleLootParamsSpacer: int

    ### MiscLootParams
    MiscLootParamsSpacer: int
    MiscLootParams: int
    helmetLossChance: int
    helmetLossSound: bool

    BMParamsSpacer2: int

    ## ExtenderParams
    ExtenderParamsSpacer: int
    ExtenderParams: int
    YourExtenderNameSpacer: object  # added in AU 12.3.0.0?
    YourExtenderNameParams: object  # added in AU 12.3.0.0?
    A3UE_YourExtenderName_ParamName: object  # added in AU 12.3.0.0?

    ## ExperimentalParams
    ExperimentalParamsSpacer: int
    ExperimentalParams: int

    ## DevelopmentParams
    DevelopmentParamsSpacer: int
    DevelopmentParams: int
    LogLevel: int
    A3A_logDebugConsole: int

    ## DeprecatedParams
    DeprecatedParams: object  # added in AU 12.3.0.0
    DeprecatedParamsSpacer: object  # added in AU 12.3.0.0

    A3A_flagGarageBlock: int

    # A3A_showGroupBar: bool  # removed in AU 12.3.0.0
