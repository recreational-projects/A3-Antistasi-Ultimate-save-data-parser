"""Tests for `params` module."""


import msgspec
import pytest

from a3_antistasi_ultimate_save_data_parser.model.params import Params
from tests.model.conftest import DictNode


class TestParams:
    """Tests for `Params` class."""

    @pytest.fixture
    def sample_params_dict(self, sample_dict: DictNode) -> DictNode:
        """Return sample data `dict`."""
        return sample_dict["params"]

    def test_sample_data_contains_all_required_params_members(
        self,
        sample_params_dict: DictNode,
    ) -> None:
        """Test that sample contains keys for all `Params` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(sample_params_dict.keys())
        required_field_names = set(Params.__annotations__.keys())
        # act
        # assert
        assert sample_data_keys.issuperset(required_field_names)

    def test_create(self, sample_params_dict: DictNode) -> None:
        """Test that `Params` can be created from sample `dict`."""
        # arrange
        # act
        my_params = msgspec.convert(sample_params_dict, type=Params)
        # assert
        assert isinstance(my_params, Params)
