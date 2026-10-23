"""The test suite."""

import json
from pathlib import Path
from typing import Any

import msgspec
import pytest

from a3_antistasi_ultimate_save_data_parser.model import Params, Position, SaveData

_JSON_SAMPLE_PATH = Path(__file__).parent / "sample.json"
"""NB: this is a composite sample and won't be internally consistent."""


@pytest.fixture
def sample_save_data_dict() -> dict[str, object]:
    """Return sample data `dict`."""
    str_ = _JSON_SAMPLE_PATH.read_text()
    return json.loads(str_)


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


class TestParams:
    """Tests for `Params` class."""

    def test_sample_data_contains_all_required_params_members(
        self,
        sample_save_data_dict: dict[str, Any],
    ) -> None:
        """Test that sample contains keys for all `Params` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(sample_save_data_dict["params"].keys())
        required_field_names = set(Params.__annotations__.keys())
        # act
        # assert
        assert sample_data_keys.issuperset(required_field_names)

    def test_create(self, sample_save_data_dict: dict[str, object]) -> None:
        """Test that `Params` can be created from sample `dict`."""
        # arrange
        # act
        my_params = msgspec.convert(sample_save_data_dict["params"], type=Params)
        # assert
        assert isinstance(my_params, Params)


class TestSaveData:
    """Tests for `SaveData` class."""

    def test_sample_data_contains_all_required_save_data_members(
        self,
        sample_save_data_dict: dict[str, object],
    ) -> None:
        """Test that sample contains keys for all `SaveData` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(sample_save_data_dict.keys())
        required_field_names = set(SaveData.__annotations__.keys())
        # act
        # assert
        assert sample_data_keys.issuperset(required_field_names)

    def test_create(self, sample_save_data_dict: dict[str, object]) -> None:
        """Test that `SaveData` can be created from sample `dict`."""
        # arrange
        # act
        my_save_data = msgspec.convert(sample_save_data_dict, type=SaveData)
        # assert
        assert isinstance(my_save_data, SaveData)

    def test_create_from_str(self) -> None:
        """Test that `SaveData` can be created from JSON `str`."""
        # arrange
        str_ = _JSON_SAMPLE_PATH.read_text()
        # act
        my_save_data = SaveData.decode_str(str_)
        # assert
        assert isinstance(my_save_data, SaveData)
