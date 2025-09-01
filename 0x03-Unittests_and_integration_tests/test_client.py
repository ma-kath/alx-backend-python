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
