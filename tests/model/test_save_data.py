"""Tests for `save_data` module."""

import datetime as dt
from typing import TYPE_CHECKING, ClassVar

import msgspec

from a3_antistasi_ultimate_save_data_parser.model.params import Params
from a3_antistasi_ultimate_save_data_parser.model.player import Player
from a3_antistasi_ultimate_save_data_parser.model.save_data import SaveData

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser.model._types import JSONDictNode


class TestSaveData:
    """Tests for `SaveData` class."""

    DERIVED_FIELDS: ClassVar[set[str]] = {"players"}

    def test_sample_data_contains_all_members(
        self,
        sample_dict: JSONDictNode,
    ) -> None:
        """Test that sample data contains keys for all non-derived `SaveData` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(sample_dict.keys())
        save_data_field_names = {f.name for f in msgspec.structs.fields(SaveData)}
        # act
        # assert
        assert sample_data_keys.issuperset(save_data_field_names - self.DERIVED_FIELDS)

    def test_decode_str(self, sample_str: str) -> None:
        """Test `SaveData.decode_str`."""
        # arrange
        # act
        my_save_data = SaveData.decode_str(sample_str)
        # assert
        assert isinstance(my_save_data, SaveData)
        assert isinstance(my_save_data.params, Params)
        assert my_save_data.saveTime == dt.datetime(
            2026, 10, 22, 14, 20, 40, 383000, tzinfo=dt.UTC
        )
        assert my_save_data.dateX == dt.datetime(2035, 6, 11, 18, 43, tzinfo=None)
        assert isinstance(my_save_data.savedPlayers[0], int)
        assert isinstance(my_save_data.membersX[0], int)
        assert isinstance(my_save_data.players[12345678901234567], Player)
