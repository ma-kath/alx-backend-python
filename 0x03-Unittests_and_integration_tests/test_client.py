#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class."""
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json):
        """Test that GOC return expected value"""
        mock_get_json.return_value = {"mocked": "data"}
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, mock_get_json.return_value)

    def test_public_repos_url(self):
        """Test to return the correct URL."""
        test_playload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        client = GithubOrgClient("testorg")
        with patch.object(
            type(client),
            "org",
            new_callable=property
        ) as mock_org:
            mock_org.return_value = test_playload
            result = client._public_repos_url
            self.assertEqual(result, test_playload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that mocked props and return once."""
        mocked_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = mocked_repos_payload
        client = GithubOrgClient("testorg")
        with patch.object(
            type(client),
            "public_repos_url",
            new_callable=property
        ) as mock_public_repos_url:
            test_url = "https://api.github.com/orgs/testorg/repos"
            mock_public_repos_url.fget = lambda self: test_url
            repos = client.public_repos()
            repos_names = [repo for repo in repos]
            expected_names = [repo["name"] for repo in mocked_repos_payload]
            self.assertEqual(repos_names, expected_names)
            self.assertEqual(mock_public_repos_url.fget.call_count, 1)
            mock_get_json.assert_called_once_with(test_url)
