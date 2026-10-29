# A3-Antistasi-Ultimate-save-data-parser

Python library to parse [Antistasi Ultimate ('AU')](https://antistasiultimate.com/) save data that's been exported from the game as JSON.
This feature was added in AU v12.2.0 (public testing only as of 2026-10-28).

Experimental/alpha. Only tested with output from AU v12.3.0.0.

* Outputs Python [msgspec.Struct](https://msgspec.dev/) classes

* Datetime fields are parsed as Python `datetime.datetime` built-in objects

* Position fields are parsed as a `Position` class with `x`, `y`, `z` fields

* `params` is parsed as a `Params` class

* SteamId64s are converted to int

* players' data is parsed to `SaveData.players`, a mapping of SteamId64: `PlayerData` class


## Installing

From GitHub, specifying a version via tag, e.g:

```shell
uv add git+https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser --tag v0.3.0
```

or with `pip`:

```shell
pip install git+https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser@v0.3.0
```


## Example code

Requires `rich` for formatting output.

```
from pathlib import Path
from rich import print as rprint

import msgspec

from a3_antistasi_ultimate_save_data_parser.save_data import SaveData

BASE_PATH = Path(__file__).parent


with (BASE_PATH / "sample.json").open() as file:
save_data_obj = SaveData.decode_str(file.read())

print("\nSOURCE JSON -> SAVEDATA OBJECT")
rprint(save_data_obj)
print("\nSAVEDATA OBJECT -> JSON")
rprint(msgspec.json.encode(save_data_obj))
```

This should display a representation of a `SaveData` object like:

```pycon
SOURCE JSON -> SAVEDATA OBJECT
SaveData(
    a3_antistasi_ultimate_save_data_parser_version='0.0.4',
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
        12345678901234567: PlayerData(
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

SAVEDATA OBJECT -> JSON
b'{"a3_antistasi_ultimate_save_data_parser_version":"0.0.4","name":"RHS PKL Unsung 1 
test","saveTime":"2026-10-22T14:20:40.383000Z","map":"rhspkl","serverID":false,"campaignID":"10ba0f24-f1cd-4e5b-a2f2-9f6822a393a8","version":"12.2.0.0","params":{"A3A_attackHQProximityMul":3,"A3A_builderAllowRoads":false,"A3A_builderBuildTime":5,"A3A_builderLimit":
300,"A3A_builderPermissions":3,"A3A_diameterExtendedCaptureArea":0,"A3A_enemyAttackMul":10,"A3A_enemyBalanceMul":11,"A3A_enemyResponseTime":10,"A3A_enemySkillMul":2,"A3A_flagGarageBlock":0,"A3A_GCThreshold":-1,"A3A_guestCommander":true,"A3A_guestItemLimit":25,"A3A_
idleTimeout":300,"A3A_invaderBalanceMul":12,"A3A_isUAVAFK":true,"A3A_isZeusAFK":true,"A3A_logDebugConsole":1,"A3A_rebelGarrisonGroupSize":8,"A3A_rebelGarrisonLimit":24,"A3A_rebelSkillMul":2,"A3A_removeRestore":false,"A3A_reviveTime":16,"A3A_roadBlocksBaseChance":0,
...
``` 
Note that the output JSON won't match the source JSON.

## License

This project is licensed under the MIT License - the same as
[Antistasi Ultimate source code](https://github.com/Antistasi-Ultimate-Community/A3-Antistasi-Ultimate).

## Development

Run tests:
```shell
uv run pytest
```

Serve docs locally:
```shell
uv run pdoc a3_antistasi_ultimate_save_data_parser
```