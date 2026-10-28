"""Tests for `player` module."""

from typing import TYPE_CHECKING

from a3_antistasi_ultimate_save_data_parser.player import Player

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode


class TestPlayer:
    """Tests for `Player` class."""

    def test_create(self, sample_dict: JSONDictNode) -> None:
        """Test that `Player` can be created from root of sample `dict`."""
        # arrange
        # act
        my_player_dict = Player._dict_from_raw_dict(sample_dict)
        # assert
        assert my_player_dict.keys() == {12345678901234567}
        assert isinstance(my_player_dict[12345678901234567], Player)
