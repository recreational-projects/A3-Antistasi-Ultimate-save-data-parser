"""Main module."""

from pathlib import Path

import msgspec
from rich import print as rprint

from .model.save_data import SaveData

BASE_PATH = Path(__file__).parent.parent.parent / "tests" / "model"


with (BASE_PATH / "sample.json").open() as file:
    save_data_obj = SaveData.decode_str(file.read())

rprint("\nSOURCE JSON -> SAVEDATA OBJECT")
rprint(save_data_obj)
rprint("\nSAVEDATA OBJECT -> JSON")
rprint(msgspec.json.encode(save_data_obj))
