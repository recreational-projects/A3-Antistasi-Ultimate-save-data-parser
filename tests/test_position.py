"""Tests for `position` module."""

import msgspec

from a3_antistasi_ultimate_save_data_parser.position import Position


class TestPosition:
    """Tests for `Position` class."""

    def test_convert_from_3_list(self) -> None:
        """Test that `Position` can be converted from 3-value `list`."""
        # arrange
        # act
        my_pos = msgspec.convert([2080.5, 7477.51, 0.00137329], type=Position)
        # assert
        assert isinstance(my_pos, Position)

    def test_convert_from_2_list(self) -> None:
        """Test that `Position` can be created from 2-value `list`."""
        # arrange
        # act
        my_pos = msgspec.convert([1977.09, 412.31], type=Position)
        # assert
        assert isinstance(my_pos, Position)
        assert my_pos.z == 0
