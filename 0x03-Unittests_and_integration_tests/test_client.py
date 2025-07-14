#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from typing import Dict, List
from fixtures import TEST_PAYLOAD
import requests


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

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Dict, license_key: str,
                         expected_result: bool) -> None:
        """
        Tests that GithubOrgClient.has_license returns the 
        correct boolean value.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


# Prepare the data for parameterized_class from TEST_PAYLOAD
integration_payloads = []
for org_data, repos_data in TEST_PAYLOAD:
    # Extract org_name from the repos_url in org_data
    # e.g., 'google' from '.../orgs/google/repos'
    org_name = org_data["repos_url"].split('/')[-2]
    expected_repos_list = [repo["name"] for repo in repos_data]
    apache2_repos_list = [
        repo["name"] for repo in repos_data
        if "license" in repo and repo["license"] and
        repo["license"]["key"] == "apache-2.0"
    ]
    integration_payloads.append({
        "org_name": org_name,
        "org_payload": org_data,
        "repos_payload": repos_data,
        "expected_repos": expected_repos_list,
        "apache2_repos": apache2_repos_list,
    })


@parameterized_class(integration_payloads)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient.public_repos method.
    Mocks external requests using requests.get.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up class-level fixtures for integration tests.
        Mocks requests.get to return predefined payloads from fixtures.
        """
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect_func(url: str) -> Mock:
            """
            Custom side effect function for requests.get mock.
            Returns different mock responses based on the URL.
            """
            mock_response = Mock()
            if url == GithubOrgClient.ORG_URL.format(org=cls.org_name):
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                # This case should ideally not be reached if URLs are correct
                raise ValueError(f"Unexpected URL in mock: {url}")
            return mock_response

        cls.mock_get.side_effect = side_effect_func

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Tear down class-level fixtures. Stops the requests.get patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """
        Tests the public_repos method in an integration context
        without a license filter.
        """
        client = GithubOrgClient(self.org_name)
        self.assertEqual(client.public_repos(), self.expected_repos)
        # Verify calls to requests.get
        calls = [
            unittest.mock.call(GithubOrgClient.ORG_URL.format(
                org=self.org_name)),
            unittest.mock.call(self.org_payload["repos_url"])
        ]
        self.mock_get.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.mock_get.call_count, 2)

    def test_public_repos_with_license(self) -> None:
        """
        Tests the public_repos method in an integration context
        with an 'apache-2.0' license filter.
        """
        client = GithubOrgClient(self.org_name)
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
        # Verify calls to requests.get
        calls = [
            unittest.mock.call(GithubOrgClient.ORG_URL.format(
                org=self.org_name)),
            unittest.mock.call(self.org_payload["repos_url"])
        ]
        self.mock_get.assert_has_calls(calls, any_order=True)
        self.assertEqual(self.mock_get.call_count, 2)
