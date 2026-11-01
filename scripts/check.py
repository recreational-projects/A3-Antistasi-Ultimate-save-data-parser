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
from itertools import chain
from pathlib import Path
from typing import TYPE_CHECKING

import msgspec

# pyrefly: ignore[missing-import]
from rich.pretty import pprint

from a3_antistasi_ultimate_save_data_parser._types import LEN_STEAM_ID64
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
    _input_dict_root_keys = input_dict.keys()

    _save_keys_intersect = _input_dict_root_keys & SaveData.__struct_fields__
    missing_root_input_keys = (
        set(SaveData.__struct_fields__) - _save_keys_intersect - SaveData.DERIVED_FIELDS
    )

    player_input_keys = {
        k
        for k in input_dict
        if k.removeprefix("player_")[LEN_STEAM_ID64 + 1 :]
        in PlayerData.__struct_fields__
    }
    extra_root_input_keys = (
        _input_dict_root_keys
        - _save_keys_intersect
        - set(PlayerData.__struct_fields__)
        - player_input_keys
    )

    _sub_params_types = Params._get_sub_params_types()
    _sub_params_handled_keys = _flattened_set(
        cls_.__struct_fields__ for cls_ in _sub_params_types.values()
    )

    params_handled_keys = (
        set(Params.__struct_fields__)
        | set(Params._DISCARDED_KEYS)
        | _sub_params_handled_keys
    ) - _sub_params_types.keys()

    _params_intersect = input_dict["params"].keys() & params_handled_keys
    missing_params_input_keys = params_handled_keys - _params_intersect
    extra_params_input_keys = input_dict["params"].keys() - _params_intersect

    print("\nInput JSON `version`:")
    pprint(input_dict["version"])

    print("\nPARAMS:")
    print("\n`Params` members missing from input `params`:")
    _print_iterable(missing_params_input_keys)
    print("\nKeys in input `params` not required by `Params`:")
    _print_iterable(extra_params_input_keys)

    print("\nAttempting to structure input dict `params` as `Params`:")
    try:
        Params._from_dict(input_dict["params"])
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


def _print_iterable(iterable: Iterable[str]) -> None:
    pprint(sorted(iterable))


def _flattened_set(iterable: Iterable[Iterable[object]]) -> set[object]:
    return set(chain.from_iterable(iterable))


if __name__ == "__main__":
    main()
