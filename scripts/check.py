"""Run with e.g.:
```
uv run scripts/check.py tests/base_sample.json
```

Uses the editable version of the package so that dev changes are reflected.
"""  # noqa: D205, D400, D415
# /// script
# dependencies = [
#     "a3-antistasi-ultimate-save-data-parser",
#     "rich>=15.0.0",
# ]
# [tool.uv.sources]
# a3-antistasi-ultimate-save-data-parser = { path = ".." , editable = true }
# ///

from argparse import ArgumentParser
from pathlib import Path
from typing import TYPE_CHECKING

import msgspec

# pyrefly: ignore[missing-import]
from rich.pretty import pprint

from a3_antistasi_ultimate_save_data_parser.params import Params
from a3_antistasi_ultimate_save_data_parser.player_data import PlayerData
from a3_antistasi_ultimate_save_data_parser.save_data import SaveData

if TYPE_CHECKING:
    from collections.abc import Iterable

PROJECT_ROOT = Path(__file__).parent.parent


def main() -> None:
    """Check that the input JSON file contains all the required fields."""
    file_path = _parse_input_path()
    input_str = file_path.read_text()
    input_dict = msgspec.json.decode(input_str)

    save_data_fields = _get_struct_field_names(SaveData)
    save_data_intersection = input_dict.keys() & save_data_fields
    missing_root_input_keys = (
        save_data_fields - save_data_intersection - SaveData.DERIVED_FIELDS
    )
    extra_root_input_keys = input_dict.keys() - save_data_intersection
    player_data_fields = {f.name for f in msgspec.structs.fields(PlayerData)}
    player_input_keys = {
        k for k in input_dict if k.removeprefix("player_")[18:] in player_data_fields
    }

    extra_root_input_keys = (
        extra_root_input_keys - player_data_fields - player_input_keys
    )

    params_fields = _get_struct_field_names(Params)
    params_intersection = input_dict["params"].keys() & params_fields
    missing_params_input_keys = params_fields - params_intersection
    extra_params_input_keys = input_dict["params"].keys() - params_intersection

    print("\nInput JSON `version`:")
    pprint(input_dict["version"])

    print("\nPARAMS:")
    print("\n`Params` members missing from input `params`:")
    _print_iterable(missing_params_input_keys)
    print("\nKeys in input `params` not required by `Params`:")
    _print_iterable(extra_params_input_keys)

    print("\nAttempting to structure input dict `params` as `Params`:")
    try:
        Params(**input_dict["params"])
        print("OK")
    except TypeError as e:
        pprint(e)

    print("\nPLAYER_DATA:")
    print("\n`PlayerData` related keys in input root:")
    _print_iterable(player_input_keys)

    print("\nSAVE_DATA:")
    print("\n`SaveData` members missing from input root:")
    _print_iterable(missing_root_input_keys)
    print("\nKeys in input root not required by `SaveData`:")
    _print_iterable(extra_root_input_keys)

    print("\nAttempting to decode input JSON `str` to `SaveData`:")
    try:
        SaveData.decode_str(input_str)
        print("OK")
    except TypeError as e:
        pprint(e)
    except msgspec.ValidationError as e:
        pprint(e)


def _parse_input_path() -> Path:
    arg_parser = ArgumentParser()
    arg_parser.add_argument("path", type=Path, help="Path to a JSON save data file")
    args = arg_parser.parse_args()
    return args.path


def _get_struct_field_names(struct_cls: type[msgspec.Struct]) -> set[str]:
    """Return the set of field names defined on a msgspec Struct."""
    return {field.name for field in msgspec.structs.fields(struct_cls)}


def _print_iterable(iterable: Iterable) -> None:
    pprint(sorted(iterable))


if __name__ == "__main__":
    main()
