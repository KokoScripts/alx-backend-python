#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """
    Tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {"repos_url": "https://api.github.com/orgs/google/repos"}),
        ("abc", {"repos_url": "https://api.github.com/orgs/abc/repos"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, expected_org_payload: Dict,
                 mock_get_json: unittest.mock.MagicMock) -> None:
        """
        Tests that GithubOrgClient.org returns the correct value
        and that get_json is called once with the expected argument.
        """
        mock_get_json.return_value = expected_org_payload
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected_org_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )


if __name__ == '__main__':
    unittest.main()

