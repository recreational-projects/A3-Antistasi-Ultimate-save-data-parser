"""Tests for `player` module."""

from typing import TYPE_CHECKING

from a3_antistasi_ultimate_save_data_parser.player_data import PlayerData

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode


class TestPlayer:
    """Tests for `PlayerData` class."""

    def test_from_raw_dict(self, base_sample_dict: JSONDictNode) -> None:
        """Test that `PlayerData` can be created from root of sample `dict`."""
        # arrange
        # act
        my_player = PlayerData._from_raw_dict(
            raw_dict=base_sample_dict, steam_id=12345678901234567
        )
        # assert
        assert isinstance(my_player, PlayerData)

    def test_dict_from_raw_dict(self, base_sample_dict: JSONDictNode) -> None:
        """Test that `PlayerData` dict can be created from root of sample `dict`."""
        # arrange
        # act
        my_player_dict = PlayerData._dict_from_raw_dict(base_sample_dict)
        # assert
        assert my_player_dict.keys() == {12345678901234567}
        assert isinstance(my_player_dict[12345678901234567], PlayerData)
