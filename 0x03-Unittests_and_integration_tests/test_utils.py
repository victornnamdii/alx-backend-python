#!/usr/bin/env python3
"""
Learning Unittests
"""

import unittest
import utils
from parameterized import parameterized
from typing import Mapping, Tuple, Union, Dict


class TestAccessNestedMap(unittest.TestCase):
    """
    Testing utils.access_nested_map method
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
            self,
            nested_map: Dict[str, Union[Dict, int]],
            path: Tuple[str],
            expected_result: Union[Dict, int]
            ) -> None:
        """
        Testing expected results
        """
        self.assertEqual(utils.access_nested_map(nested_map, path),
                         expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict[str, Union[Dict, int]],
            path: Tuple[str],
            exception: Exception
            ) -> None:
        """
        Testing exceptions
        """
        with self.assertRaises(exception):
            utils.access_nested_map(nested_map, path)
