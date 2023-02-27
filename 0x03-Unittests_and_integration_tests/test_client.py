#!/usr/bin/env python3
"""
Learning Unittests and Integration Tests
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized
from typing import Dict, Callable


class TestGithubOrgClient(unittest.TestCase):
    """
    Testing GitHubOrgClient
    """
    @parameterized.expand([
        ("google", {"login": "google", "id": 1342004,
                    "repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"login": "abc", "id": 1342555,
                 "repos_url": "https://api.github.com/orgs/abc/repos"})
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

    def test_public_repos_url(self):
        """
        Testing GithubOrgClient._public_repos_url
        """
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_property:
            mock_property.return_value = {
                "login": "google", "id": 1342004,
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/orgs/google/repos")
