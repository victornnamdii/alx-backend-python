#!/usr/bin/env python3
"""
Learning Unittests and Integration Tests
"""

import unittest
from unittest.mock import patch, Mock
from client import GithubOrgClient
from parameterized import parameterized
from typing import Dict, Callable


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing GitHubOrgClient
    """
    @parameterized.expand([
        ("google", {"login": "google", "id": 1342004}),
        ("abc", {"login": "abc", "id": 1342555})
    ])
    @patch(
        "client.get_json",
    )
    def test_org(
            self,
            org: str,
            response: Dict,
            mocked_fn: Mock) -> None:
        """
        Testing the GithubOrgClient.org method
        """
        mocked_fn.return_value = response
        organisation = GithubOrgClient(org)
        self.assertEqual(organisation.org, response)
        mocked_fn.assert_called_once()
