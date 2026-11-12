# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.11.0] - 2026-11-12

### Added

* `ParamsCategory` class to public API

### Fixed

* Parsing failed if extender `A3UE_*` params were present. For now, these params are ignored.


## [0.10.0] - 2026-11-11

### Added

* `SaveData.from_json_file()`
* Ignore `A3UE_YourExtenderName_ParamName` param and related non-data params: 
  probably placeholders introduced by an in-development A3U extender

### Changed

* `SaveData.decode_str()` renamed to `SaveData.from_json_str()`
* docs: improved documentation
* tests: base JSON test data is now from AU 12.4.1 default game


## [0.9.1] - 2026-11-10

### Fixed

* `SaveData` failed to parse if `DLC` was populated. Now parsed to `list[str]` instead of `list[int]`


## [0.9.0] - 2026-11-09

### Added

* extract `SaveData.posHQ` class
* improve position handling


## [0.8.0] - 2026-11-05

### Added

* support AU 12.4.0.0 (adds `SaveData.params.bm.A3A_ultimate_disableBazaar`)
* improve `Params` validation and error message
* validate `SteamID64` as 17 digits
* make `types` module public
* docs: improved documentation
* ci: also run on Python 3.14

### Fixed

* `scripts/check.py` didn't reflect code changes


## [0.7.0] - 2026-11-03

### Added

* `SaveData.params` handles missing `A3UE_YourExtenderName_ParamName` placeholder param
* `SaveData.params` discards `A3A_showGroupBar` removed from AU v12.3.0.0
  (as it can probably still appear in exports from AU >= v12.3.0.0, if made from existing AU < 12.3.0.0 saves) 


## [0.6.0] - 2026-11-02

### Added

* validate `SaveData.players`
* `SaveData.posHQ`: parse `Position`s
* `SaveData.campaignID`: parse as `uuid.UUID`
* docs: improved documentation and type hints

### Changed

* `SaveData.traderPosition` parsed to `Position2D`, instead of `Position` with `z==0`


## [0.5.0] - 2026-11-01

### Added

* `SaveData.params`: hierarchical structure; discard source data that doesn't contain actual information
  (artifacts of the Antistasi Ultimate Params dialog layout)
* `SaveData.DERIVED_FIELDS` class variable renamed to `SaveData.__DERIVED_FIELDS__`
* improved robustness, tests and type hints
* docs: improved documentation
* ci: pin exact versions of dev/CI dependencies

## [0.4.0] - 2026-10-30

### Added

* `SaveData.A3A_fuelAmountleftArray`: positions are parsed to `Position`s
* docs: improved documentation

### Fixed

* `SaveData` failed to parse if `serverID` was a string. Now parsed to `str` or `Literal[False]`
* docs: indentation error in `README.md` sample code


## [0.3.0] - 2026-10-29

### Added

* supplementary `scripts/check.py` to identify potential parsing issues in a save data JSON file
* sort `Params` members by their appearance in AU params screens
* `py.typed` marker, enabling downstream type checking
* docs: `README.md` explains AU version support

### Changed

* support only Antistasi Ultimate 12.3.0.0 JSON save data output

### Removed

* redundant `[project.scripts]` table from `pyproject.toml`


## [0.2.0] - 2026-10-28

### Added

* [documentation website](https://recreational-projects.github.io/A3-Antistasi-Ultimate-save-data-parser/)
* project metadata
* test coverage

### Changed

* renamed `Player` to `PlayerData`
* renamed `SaveData.a3_antistasi_ultimate_save_data_parser_version`
 to `__a3_antistasi_ultimate_save_data_parser_version__` to keep it out of the main namespace

### Fixed

* `SaveData` parsing failed on `'traderPosition': []` - is now parsed as `None` 

### Removed

* `Player` constructor from documented API


## [0.1.0] - 2026-10-28

Initial documented version


[0.11.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.10.0..v0.11.0
[0.10.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.9.1..v0.10.0
[0.9.1]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.9.0..v0.9.1
[0.9.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.8.0..v0.9.0
[0.8.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.7.0..v0.8.0
[0.7.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.6.0..v0.7.0
[0.6.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.5.0..v0.6.0
[0.5.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.4.0..v0.5.0
[0.4.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.3.0..v0.4.0
[0.3.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.2.0..v0.3.0
[0.2.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.1.0..v0.2.0
[0.1.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/releases/tag/v0.1.0
