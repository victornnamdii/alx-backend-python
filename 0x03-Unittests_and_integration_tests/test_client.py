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


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ Class for Integration test of fixtures """

    @classmethod
    def setUpClass(cls) -> None:
        """A class method called before tests in an individual class are run"""
        config = {'return_value.json.side_effect':
                  [
                      cls.org_payload, cls.repos_payload,
                      cls.org_payload, cls.repos_payload
                  ]
                  }
        cls.get_patcher = patch('requests.get', **config)

        cls.mock = cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """ Integration test: public repos"""
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.org, self.org_payload)
        self.assertEqual(test_class.repos_payload, self.repos_payload)
        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.mock.assert_called()

    def test_public_repos_with_license(self) -> None:
        """ Integration test for public repos with License """
        test_class = GithubOrgClient("google")

        self.assertEqual(test_class.public_repos(), self.expected_repos)
        self.assertEqual(test_class.public_repos("XLICENSE"), [])
        self.assertEqual(test_class.public_repos(
            "apache-2.0"), self.apache2_repos)
        self.mock.assert_called()

    @classmethod
    def tearDownClass(cls) -> None:
        """A class method called after tests in an individual class have run"""
        cls.get_patcher.stop()
