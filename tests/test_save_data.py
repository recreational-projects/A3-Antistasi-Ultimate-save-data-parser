"""Tests for `save_data` module."""

import datetime as dt
import json
from pathlib import Path
from typing import TYPE_CHECKING
from uuid import UUID

import msgspec
import pytest

from a3_antistasi_ultimate_save_data_parser.params import Params
from a3_antistasi_ultimate_save_data_parser.player_data import PlayerData
from a3_antistasi_ultimate_save_data_parser.position import Position, Position2D
from a3_antistasi_ultimate_save_data_parser.save_data import PosHQ, SaveData

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser.types import _JSONDictNode


_JSON_OVERRIDES_PATH = Path(__file__).parent / "overrides.json"
"""NB: this is a composite sample and won't be internally consistent."""
_PACKAGE_MINOR_VERSION = "0.10"


class TestSaveData:
    """Tests for `SaveData` class."""

    def test_base_sample_data_contains_all_members(
        self,
        base_sample_dict: _JSONDictNode,
    ) -> None:
        """Test that sample data contains keys for all non-derived `SaveData` fields.

        Does not recurse.
        """
        # arrange
        sample_data_root_keys = set(base_sample_dict.keys())
        save_data_field_names = {f.name for f in msgspec.structs.fields(SaveData)}
        # act
        # assert
        assert sample_data_root_keys.issuperset(
            save_data_field_names - SaveData.__DERIVED_FIELDS__
        )

    def test_from_json_file(self, base_sample_path: Path) -> None:
        """Test `SaveData.from_json_file()`."""
        # arrange
        # act
        sd = SaveData.from_json_file(base_sample_path)
        # assert
        assert isinstance(sd, SaveData)

    def test_from_json_str(self, base_sample_str: str) -> None:
        """Test `SaveData.from_json_str()`."""
        # arrange
        # act
        sd = SaveData.from_json_str(base_sample_str)
        # assert
        assert isinstance(sd, SaveData)
        assert sd.__a3_antistasi_ultimate_save_data_parser_version__.split(".")[
            0:2
        ] == _PACKAGE_MINOR_VERSION.split(".", maxsplit=1)
        assert isinstance(sd.saveTime, dt.datetime)
        assert sd.saveTime.tzinfo == dt.UTC
        assert isinstance(sd.campaignID, UUID)
        assert isinstance(sd.membersX[0], int)
        assert isinstance(sd.savedPlayers[0], int)
        assert isinstance(sd.players[12345678901234567], PlayerData)
        assert isinstance(sd.dateX, dt.datetime)
        assert sd.dateX.tzinfo is None
        assert isinstance(sd.posHQ, PosHQ)
        assert sd.aggressionOccupants == [1, []]
        assert sd.traderPosition is None
        assert _A3A_fuelAmountleftArray_conforms_to_type(sd.A3A_fuelAmountleftArray)
        assert isinstance(sd.params, Params)

    @pytest.fixture
    def complex_sample_str(self, base_sample_dict: _JSONDictNode) -> str:
        """Return sample data `str`."""
        dict_ = base_sample_dict.copy()
        overrides = msgspec.json.decode(_JSON_OVERRIDES_PATH.read_text())
        dict_.update(**overrides)
        return json.dumps(dict_)

    def test_decode_complex_sample_str(self, complex_sample_str: str) -> None:
        """Test `SaveData.decode_str`."""
        # arrange
        # act
        sd = SaveData.from_json_str(complex_sample_str)
        # assert
        assert isinstance(sd, SaveData)
        assert sd.aggressionOccupants == [1, [[19.2, -0.2], [-4.25, 0.25]]]
        assert isinstance(sd.traderPosition, Position2D)
        assert _A3A_fuelAmountleftArray_conforms_to_type(sd.A3A_fuelAmountleftArray)
        assert isinstance(sd.params, Params)


def _A3A_fuelAmountleftArray_conforms_to_type(
    value: list[tuple[Position, float]],
) -> bool:
    return all(
        (
            isinstance(value, list),
            all(isinstance(item, tuple) for item in value),
            all(isinstance(item[0], Position) for item in value),
            all(isinstance(item[1], float) for item in value),
        )
    )
