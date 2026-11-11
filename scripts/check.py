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

from a3_antistasi_ultimate_save_data_parser.params import Params
from a3_antistasi_ultimate_save_data_parser.player_data import (
    _SOURCE_PLAYER_FIELDS_PREFIX,
    _steam_id_64_from_player_data_key,
)
from a3_antistasi_ultimate_save_data_parser.save_data import SaveData

if TYPE_CHECKING:
    from collections.abc import Iterable

PROJECT_ROOT = Path(__file__).parent.parent


def main() -> None:
    """Check that the input JSON file contains all the required fields."""
    path = _parse_input_path()
    if not path.is_file():
        err_msg = f"Input path '{path}' is not a file."
        raise ValueError(err_msg)

    input_str = path.read_text()
    input_dict = msgspec.json.decode(input_str)

    print("\nInput JSON AU `version`:")
    pprint(input_dict["version"])

    missing_root_input_keys = (
        set(SaveData.__struct_fields__)
        - SaveData.__DERIVED_FIELDS__
        - set(input_dict.keys())
    )
    player_input_keys = {
        key
        for key in input_dict
        if key.startswith(_SOURCE_PLAYER_FIELDS_PREFIX)
        and _steam_id_64_from_player_data_key(key)
    }
    extra_root_input_keys = (
        set(input_dict.keys()) - set(SaveData.__struct_fields__) - player_input_keys
    )
    print("\nSAVE_DATA:")
    print("\n`SaveData` members missing from input root:")
    _print_iterable(missing_root_input_keys)
    print("\nKeys in input root not required by `SaveData`:")
    _print_iterable(extra_root_input_keys)

    _sub_params_types = Params._get_sub_params_types()
    _sub_params_handled_keys = _flattened_set(
        cls_.__struct_fields__ for cls_ in _sub_params_types.values()
    )
    params_handled_keys = (
        set(Params.__struct_fields__)
        | set(Params._DISCARD_KEYS)
        | _sub_params_handled_keys
    ) - _sub_params_types.keys()
    missing_params_input_keys = (
        params_handled_keys - input_dict["params"].keys() - Params._DISCARD_KEYS
    )
    extra_params_input_keys = (
        input_dict["params"].keys() - params_handled_keys - player_input_keys
    )

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
    print("\nAttempting to decode input JSON `str` to `SaveData`:")
    try:
        SaveData.from_json_str(input_str)
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
