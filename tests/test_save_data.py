"""Tests for `save_data` module."""

import datetime as dt
from typing import TYPE_CHECKING, ClassVar

import msgspec

from a3_antistasi_ultimate_save_data_parser.params import Params
from a3_antistasi_ultimate_save_data_parser.player_data import PlayerData
from a3_antistasi_ultimate_save_data_parser.save_data import SaveData

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode

PACKAGE_MINOR_VERSION = "0.1.x"


class TestSaveData:
    """Tests for `SaveData` class."""

    DERIVED_FIELDS: ClassVar[set[str]] = {
        "__a3_antistasi_ultimate_save_data_parser_version__",
        "players",
    }

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
        _pkg_minor_version = PACKAGE_MINOR_VERSION.split(".")[0:2]
        assert (
            my_save_data.__a3_antistasi_ultimate_save_data_parser_version__.split(".")[
                0:2
            ]
            == _pkg_minor_version
        )
        assert my_save_data.saveTime == dt.datetime(
            2026, 10, 22, 14, 20, 40, 383000, tzinfo=dt.UTC
        )
        assert my_save_data.dateX == dt.datetime(2035, 6, 11, 18, 43, tzinfo=None)
        assert isinstance(my_save_data.savedPlayers[0], int)
        assert isinstance(my_save_data.membersX[0], int)
        assert isinstance(my_save_data.players[12345678901234567], PlayerData)
