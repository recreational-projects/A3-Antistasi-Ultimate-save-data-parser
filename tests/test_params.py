"""Tests for `params` module."""

from typing import TYPE_CHECKING

import pytest

from a3_antistasi_ultimate_save_data_parser.params import (
    _DISCARDED_KEYS,
    AIParams,
    BasicParams,
    BMParams,
    BuilderParams,
    DeprecatedParams,
    DevelopmentParams,
    ExperimentalParams,
    ExtenderParams,
    LootParams,
    Params,
)

if TYPE_CHECKING:
    from a3_antistasi_ultimate_save_data_parser._types import JSONDictNode


class TestParams:
    """Tests for `Params` class."""

    @pytest.fixture
    def base_sample_params_dict(self, base_sample_dict: JSONDictNode) -> JSONDictNode:
        """Return sample data `dict`."""
        return base_sample_dict["params"]

    def test_sample_data_keys_match_members(
        self,
        base_sample_params_dict: JSONDictNode,
    ) -> None:
        """Test that sample data root keys match expected `Param` fields."""
        # arrange
        source_keys = set(base_sample_params_dict.keys())
        handled_keys = set(Params.__struct_fields__) | set(_DISCARDED_KEYS)
        handled_keys.difference_update(
            {
                "basic",
                "ai",
                "bm",
                "builder",
                "loot",
                "extender",
                "experimental",
                "deprecated",
                "development",
            }
        )
        handled_keys.update(
            set(BasicParams.__struct_fields__)
            | set(AIParams.__struct_fields__)
            | set(BMParams.__struct_fields__)
            | set(BuilderParams.__struct_fields__)
            | set(LootParams.__struct_fields__)
            | set(ExtenderParams.__struct_fields__)
            | set(ExperimentalParams.__struct_fields__)
            | set(DeprecatedParams.__struct_fields__)
            | set(DevelopmentParams.__struct_fields__)
        )
        # act
        # assert
        assert source_keys == handled_keys

    def test_from_dict(self, base_sample_params_dict: JSONDictNode) -> None:
        """Test that `Params` can be created from sample `dict`."""
        # arrange
        # act
        my_params = Params._from_dict(base_sample_params_dict)
        # assert
        assert isinstance(my_params, Params)
        assert isinstance(my_params.basic, BasicParams)
        assert isinstance(my_params.ai, AIParams)
        assert isinstance(my_params.bm, BMParams)
        assert isinstance(my_params.builder, BuilderParams)
        assert isinstance(my_params.loot, LootParams)
        assert isinstance(my_params.extender, ExtenderParams)
        assert isinstance(my_params.experimental, ExperimentalParams)
        assert isinstance(my_params.deprecated, DeprecatedParams)
        assert isinstance(my_params.development, DevelopmentParams)

    def test_all_relevant_source_keys_included(
        self, base_sample_params_dict: JSONDictNode
    ) -> None:
        """TODO."""
        # arrange
        relevant_source_keys = set(base_sample_params_dict.keys()) - _DISCARDED_KEYS
        # act
        my_params = Params._from_dict(base_sample_params_dict)
        # assert
        my_params_relevant_keys = (
            set(my_params.__struct_fields__)
            | set(BasicParams.__struct_fields__)
            | set(AIParams.__struct_fields__)
            | set(BMParams.__struct_fields__)
            | set(BuilderParams.__struct_fields__)
            | set(LootParams.__struct_fields__)
            | set(ExtenderParams.__struct_fields__)
            | set(ExperimentalParams.__struct_fields__)
            | set(DeprecatedParams.__struct_fields__)
            | set(DevelopmentParams.__struct_fields__)
        ) - {
            "basic",
            "ai",
            "bm",
            "builder",
            "loot",
            "extender",
            "experimental",
            "deprecated",
            "development",
        }

        assert my_params_relevant_keys == relevant_source_keys
