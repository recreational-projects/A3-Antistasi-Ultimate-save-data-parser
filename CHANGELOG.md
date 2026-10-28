# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project tries to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


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


[0.2.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/compare/v0.1.0..v0.2.0
[0.1.0]: https://github.com/recreational-projects/A3-Antistasi-Ultimate-save-data-parser/releases/tag/v0.1.0
