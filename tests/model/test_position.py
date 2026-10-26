"""Tests for `position` module."""

from a3_antistasi_ultimate_save_data_parser.model.position import Position


class TestPosition:
    """Tests for `Position` class."""

    def test_create(self) -> None:
        """Test that `Position` can be created from 3-value `list`."""
        # arrange
        # act
        my_pos = Position.convert([2080.5, 7477.51, 0.00137329])
        # assert
        assert isinstance(my_pos, Position)

    def test_create_from_2_values(self) -> None:
        """Test that `Position` can be created from 2-value `list`."""
        # arrange
        # act
        my_pos = Position.convert([1977.09, 412.31])
        # assert
        assert isinstance(my_pos, Position)
        assert my_pos.z == 0
