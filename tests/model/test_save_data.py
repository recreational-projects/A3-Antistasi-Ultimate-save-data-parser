"""Tests for `save_data` module."""

import datetime as dt
from typing import TYPE_CHECKING

import msgspec

from a3_antistasi_ultimate_save_data_parser.model.params import Params
from a3_antistasi_ultimate_save_data_parser.model.save_data import Position, SaveData

if TYPE_CHECKING:
    from tests.model.conftest import DictNode


class TestPosition:
    """Tests for `Position` class."""

    def test_create(self) -> None:
        """Test that `Position` can be created from 3-value `list`."""
        # arrange
        # act
        my_pos = msgspec.convert([2080.5, 7477.51, 0.00137329], type=Position)
        # assert
        assert isinstance(my_pos, Position)

    def test_create_from_2_values(self) -> None:
        """Test that `Position` can be created from 2-value `list`."""
        # arrange
        # act
        my_pos = msgspec.convert([1977.09, 412.31], type=Position)
        # assert
        assert isinstance(my_pos, Position)
        assert my_pos.z == 0


class TestSaveData:
    """Tests for `SaveData` class."""

    def test_sample_data_contains_all_members(
        self,
        sample_dict: DictNode,
    ) -> None:
        """Test that sample data contains keys for all `SaveData` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(sample_dict.keys())
        save_data_field_names = {f.name for f in msgspec.structs.fields(SaveData)}
        # act
        # assert
        assert sample_data_keys.issuperset(save_data_field_names)

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
        assert my_save_data.dateX == dt.datetime(2035, 6, 11, 18, 43, tzinfo=dt.UTC)
