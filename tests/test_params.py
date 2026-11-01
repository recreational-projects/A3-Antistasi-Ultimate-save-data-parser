"""Tests for `params` module."""

from itertools import chain
from typing import TYPE_CHECKING

import pytest

from a3_antistasi_ultimate_save_data_parser.params import Params

if TYPE_CHECKING:
    from collections.abc import Iterable

    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode


class TestParams:
    """Tests for `Params` class."""

    @pytest.fixture
    def source_dict(self, base_sample_dict: JSONDictNode) -> JSONDictNode:
        """Return sample data `dict`."""
        return base_sample_dict["params"]

    def test_sample_data_keys_match_members(self, source_dict: JSONDictNode) -> None:
        """Test that sample data root keys match expected `Param` fields."""
        # arrange
        _sub_params_types = Params._get_sub_params_types()
        _sub_params_handled_keys = _flattened_set(
            cls_.__struct_fields__ for cls_ in _sub_params_types.values()
        )
        handled_keys = (
            set(Params.__struct_fields__)
            | set(Params._DISCARD_KEYS)
            | _sub_params_handled_keys
        ) - _sub_params_types.keys()
        # act
        # assert
        assert source_dict.keys() == handled_keys

    def test_from_dict(self, source_dict: JSONDictNode) -> None:
        """Test that `Params` can be created from sample `dict`."""
        # arrange
        # act
        my_params = Params._from_dict(source_dict)
        # assert
        assert my_params
        assert my_params.A3A_flagGarageBlock == 0
        _sub_params_types = Params._get_sub_params_types()
        for sub_param in _sub_params_types:
            assert isinstance(
                getattr(my_params, sub_param), _sub_params_types[sub_param]
            )
        assert my_params.basic.gameMode == 1

    def test_all_relevant_source_keys_included(self, source_dict: JSONDictNode) -> None:
        """Test that a Params instance includes all relevant source keys."""
        # arrange
        # act
        my_params = Params._from_dict(source_dict)
        # assert
        _sub_params_types = Params._get_sub_params_types()
        _my_params_sub_params_relevant_keys = set(
            chain.from_iterable(
                getattr(my_params, sub_param).__struct_fields__
                for sub_param in _sub_params_types
            )
        )
        my_params_relevant_keys = (
            set(my_params.__struct_fields__) | _my_params_sub_params_relevant_keys
        ) - _sub_params_types.keys()
        assert my_params_relevant_keys == set(source_dict.keys()) - Params._DISCARD_KEYS


def _flattened_set(iterable: Iterable[Iterable[object]]) -> set[object]:
    return set(chain.from_iterable(iterable))
