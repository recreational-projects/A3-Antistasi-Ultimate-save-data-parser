"""Tests for `save_data` module."""

import datetime as dt
import json
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar

import msgspec
import pytest

from a3_antistasi_ultimate_save_data_parser.params import Params
from a3_antistasi_ultimate_save_data_parser.player_data import PlayerData
from a3_antistasi_ultimate_save_data_parser.save_data import SaveData

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode


_JSON_OVERRIDES_PATH = Path(__file__).parent / "overrides.json"
"""NB: this is a composite sample and won't be internally consistent."""
_PACKAGE_MINOR_VERSION = "0.1.x"


class TestSaveData:
    """Tests for `SaveData` class."""

    DERIVED_FIELDS: ClassVar[set[str]] = {
        "__a3_antistasi_ultimate_save_data_parser_version__",
        "players",
    }

    def test_base_sample_data_contains_all_members(
        self,
        base_sample_dict: JSONDictNode,
    ) -> None:
        """Test that sample data contains keys for all non-derived `SaveData` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(base_sample_dict.keys())
        save_data_field_names = {f.name for f in msgspec.structs.fields(SaveData)}
        # act
        # assert
        assert sample_data_keys.issuperset(save_data_field_names - self.DERIVED_FIELDS)

    def test_decode_base_sample_str(self, base_sample_str: str) -> None:
        """Test `SaveData.decode_str`."""
        # arrange
        # act
        sd = SaveData.decode_str(base_sample_str)
        # assert
        assert isinstance(sd, SaveData)
        assert isinstance(sd.params, Params)
        _pkg_minor_version = _PACKAGE_MINOR_VERSION.split(".")[0:2]
        assert (
            sd.__a3_antistasi_ultimate_save_data_parser_version__.split(".")[0:2]
            == _pkg_minor_version
        )
        assert sd.aggressionOccupants == [1, []]
        assert sd.A3A_fuelAmountleftArray == []
        assert sd.saveTime == dt.datetime(
            2026, 10, 22, 14, 20, 40, 383000, tzinfo=dt.UTC
        )
        assert sd.dateX == dt.datetime(2035, 6, 11, 18, 43, tzinfo=None)
        assert isinstance(sd.savedPlayers[0], int)
        assert isinstance(sd.membersX[0], int)
        assert isinstance(sd.players[12345678901234567], PlayerData)

    @pytest.fixture
    def complex_sample_str(self, base_sample_dict: JSONDictNode) -> str:
        """Return sample data `str`."""
        dict_ = base_sample_dict.copy()
        overrides = msgspec.json.decode(_JSON_OVERRIDES_PATH.read_text())
        dict_.update(**overrides)
        return json.dumps(dict_)

    def test_decode_complex_sample_str(self, complex_sample_str: str) -> None:
        """Test `SaveData.decode_str`."""
        # arrange
        # act
        sd = SaveData.decode_str(complex_sample_str)
        # assert
        assert isinstance(sd, SaveData)
        assert isinstance(sd.params, Params)
        assert sd.aggressionOccupants == [1, [[19.2, -0.2], [-4.25, 0.25]]]
        assert _is_list_of_list(sd.A3A_fuelAmountleftArray)


def _is_list_of_list(obj: object) -> bool:
    """Return True if `obj` is a list of lists."""
    return isinstance(obj, list) and all(isinstance(item, list) for item in obj)
