#!/usr/bin/env python3
"""
Learning Unittests
"""

import unittest
import utils
from parameterized import parameterized
from typing import Mapping, Tuple, Union, Dict
from unittest.mock import Mock, patch


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


class TestGetJson(unittest.TestCase):
    """
    Testing utils.get_json method
    """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict[str, bool]
            ) -> None:
        """
        Testing expected result
        """
        attrs = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**attrs)) as mock_get:
            self.assertEqual(utils.get_json(test_url), test_payload)
            mock_get.assert_called_once_with(test_url)
