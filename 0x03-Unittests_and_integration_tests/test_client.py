#!/usr/bin/env python3
"""
Learning Unittests and Integration Tests
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized, parameterized_class
from typing import Dict, Callable
from fixtures import TEST_PAYLOAD


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

    @patch(
            "client.get_json",
    )
    def test_public_repos(self, mocked_get_json: Mock):
        """
        Testing GithubOrgClient.public_repos
        """
        mocked_get_json.return_value = [
            {
                "name": "truth",
                "license": {
                    "key": "apache-2.0",
                    "name": "Apache License 2.0",
                    "spdx_id": "Apache-2.0",
                    "url": "https://api.github.com/licenses/apache-2.0",
                    "node_id": "MDc6TGljZW5zZTI="
                }
            },
            {
                "name": "ruby-openid-apps-discovery",
                "license": None
            }
        ]
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mocked_repos:
            mocked_repos.return_value =\
                "https://api.github.com/orgs/google/repos"
            org = GithubOrgClient("google")
            self.assertEqual(org.public_repos(), ["truth",
                                                  "ruby-openid-apps-discovery"]
                             )
            mocked_get_json.assert_called_once()
            mocked_repos.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo: Dict[str, Dict],
                         license_key: str, expected: bool) -> None:
        """
        Testing GithubOrgClient.has_license
        """
        client_license = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(client_license, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for GithubOrgClient
    """
    @classmethod
    def setUpClass(cls) -> None:
        """
        Before tests
        """
        attrs = {'return_value.json.side_effect':
                 [
                    cls.org_payload,
                    cls.repos_payload,
                    cls.expected_repos,
                    cls.apache2_repos
                 ]}
        cls.get_patcher = patch('requests.get', **attrs)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """
        Testing GithubOrgClient.public_repos
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self) -> None:
        """
        Testing GithubOrgClient.public_repos with license parsed
        """
        self.assertEqual(
            GithubOrgClient('google').public_repos(license='apache-2.0'),
            self.apache2_repos
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """
        After Tests
        """
        cls.get_patcher.stop()
