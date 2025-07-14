#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict, List


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

    def test_public_repos_url(self) -> None:
        """
        Tests that _public_repos_url returns the expected URL
        based on a mocked org property.
        """
        # Define the payload that the mocked org property will return
        expected_payload = {
            "repos_url": "https://api.github.com/users/test_org/repos"
            }

        # Use patch as a context manager to mock the 'org' property
        # PropertyMock is used because 'org' is a memoized property
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = expected_payload
            client = GithubOrgClient("test_org")
            # Access the _public_repos_url property
            result = client._public_repos_url
            self.assertEqual(result, expected_payload["repos_url"])
            # Ensure that the 'org' property was accessed
            mock_org.assert_called_once()

    @patch('client.get_json')
    def test_public_repos(self,
                          mock_get_json: unittest.mock.MagicMock) -> None:
        """
        Tests that GithubOrgClient.public_repos returns the expected list of
        repositories. Mocks get_json and _public_repos_url to control test
        data.
        """
        # Define the payload that get_json (mocking repos_payload) will return
        test_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": None},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = test_payload

        # Define the URL that _public_repos_url (mocked property) will return
        expected_repos_url = "https://api.github.com/orgs/test_org/repos"

        # Use patch as a context manager to mock the _public_repos_url property
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = expected_repos_url

            client = GithubOrgClient("test_org")
            # Call the public_repos method
            repos = client.public_repos()

            # Assert that the list of repos is as expected
            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            # Assert that the mocked _public_repos_url property was called once
            mock_public_repos_url.assert_called_once()

            # Assert that get_json was called once with the expected URL
            # Note: get_json is called by repos_payload,
            # which uses _public_repos_url
            mock_get_json.assert_called_once_with(expected_repos_url)
