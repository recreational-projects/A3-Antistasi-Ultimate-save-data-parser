# A3-Antistasi-Ultimate-save-data-parser

Proof-of-concept to parse [Antistasi Ultimate ('AU')](https://antistasiultimate.com/) save data
that's been exported from the game as JSON
(this feature is currently only implemented in AU public test versions).

* Outputs Python [msgspec.Struct](https://msgspec.dev/) classes

* Datetime fields are parsed as Python `datetime.datetime` built-in objects

* Position fields are parsed as a `Position` class with `x`, `y`, `z` fields

* `params` is parsed as a `Params` class

* SteamId64s are converted to int

* players' data is parsed to `SaveData.players`, a mapping of SteamId64: `Player` class


## Usage

These instructions assume you have [uv](http://docs.astral.sh/uv/) installed.

* Clone/download this repo and `cd` into it.

* Run the demo script which parses a sample save data file
  (currently a composite of multiple real savegames to get a spread of test data,
  so won't make sense as a whole) 

```shell
uv run -m a3_antistasi_ultimate_save_data_parser.main
```

This should display a representation of a `SaveData` object like:
```pycon
SaveData(
    name='RHS PKL Unsung 1 test',
    saveTime=datetime.datetime(2026, 10, 22, 14, 20, 40, 383000, tzinfo=datetime.timezone.utc),
    map='rhspkl',
    serverID=False,
    campaignID='10ba0f24-f1cd-4e5b-a2f2-9f6822a393a8',
    version='12.2.0.0',
    params=Params(
        A3A_attackHQProximityMul=3,
        A3A_builderAllowRoads=False,
        A3A_builderBuildTime=5,
        ...
        A3U_blackMarketDiscountVehicle=0,
        A3U_blackMarketDiscountWeapon=0,
        A3U_disableMortars=False,
        ...
     ),
    factions=['USA_USMC', 'VN_PAVN', 'VN_VM', 'VN_Civ', 'UNS_RIV_SVR'],
    hr=180,
    resourcesFIA=11527,
    skillFIA=7,
    randomizeRebelLoadoutUniforms=True,
    petrosPosition=Position(x=2080.5, y=7477.51, z=0.00137329),
    membersX=[12345678901234567],
    savedPlayers=[12345678901234567],
    players={
        12345678901234567: Player(
            scorePlayer=462,
            loadoutPlayer=[
            ..
            ],
            moneyX=4304,
            personalGarage=[],
            pluginsData={},
            rankPlayer='SERGEANT'
        )
    },
    ...
)
``` 
## Development

Run tests:
```shell
uv run pytest
```
