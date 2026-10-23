"""Main module."""

from pathlib import Path

from rich import print as rprint

from .model.save_data import SaveData

BASE_PATH = Path(__file__).parent.parent.parent / "tests" / "model"


with (BASE_PATH / "sample.json").open() as file:
    save_data_obj = SaveData.decode_str(file.read())

rprint(save_data_obj)
