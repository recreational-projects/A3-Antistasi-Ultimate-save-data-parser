"""Tests for `params` module."""

from typing import TYPE_CHECKING

import msgspec
import pytest

from a3_antistasi_ultimate_save_data_parser.model.params import Params

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser.model._types import JSONDictNode


class TestParams:
    """Tests for `Params` class."""

    @pytest.fixture
    def sample_params_dict(self, sample_dict: JSONDictNode) -> JSONDictNode:
        """Return sample data `dict`."""
        return sample_dict["params"]

    def test_sample_data_contains_all_members(
        self,
        sample_params_dict: JSONDictNode,
    ) -> None:
        """Test that sample data contains keys for all `Params` fields.

        Does not recurse.
        """
        # arrange
        sample_data_keys = set(sample_params_dict.keys())
        save_data_field_names = {f.name for f in msgspec.structs.fields(Params)}
        # act
        # assert
        assert sample_data_keys.issuperset(save_data_field_names)

    def test_convert_from_dict(self, sample_params_dict: JSONDictNode) -> None:
        """Test that `Params` can be created from sample `dict`."""
        # arrange
        # act
        my_params = msgspec.convert(sample_params_dict, type=Params)
        # assert
        assert isinstance(my_params, Params)

    def test_all_sample_keys_included(self, sample_params_dict: JSONDictNode) -> None:
        """TODO."""
        # arrange

        # act
        my_params = msgspec.convert(sample_params_dict, type=Params)
        # assert
        _my_params_field_names = {f.name for f in msgspec.structs.fields(my_params)}
        assert _my_params_field_names == sample_params_dict.keys()
