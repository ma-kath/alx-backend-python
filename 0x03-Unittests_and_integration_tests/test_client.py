#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from unittest.mock import patch, MagicMock, PropertyMock
from parameterized import parameterized, parameterized_class
import requests
import fixtures
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
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = test_playload
            result = client._public_repos_url
            self.assertEqual(result, test_playload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that mocked props and return once."""
        mocked_repos_payload = [
            {"name": "publicrepo"},
            {"name": "publicrepo2"},
        ]
        mock_get_json.return_value = mocked_repos_payload
        client = GithubOrgClient("testorg")
        with patch.object(
            type(client),
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            test_url = "https://api.github.com/orgs/testorg/repos"
            mock_public_repos_url.return_value = test_url
            repos = client.public_repos()
            repos_names = [repo for repo in repos]
            expected_names = [repo["name"] for repo in mocked_repos_payload]
            self.assertEqual(repos_names, expected_names)
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

    def has_license(self, repo, license_key):
        """Test GithubOrgClient.has_license defined."""
        return repo.get("license", {}).get("key") == license_key

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license returns expected boolean."""
        client = GithubOrgClient("testorg")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


fi = fixtures.TEST_PAYLOAD[0]
org_payload, repos_payload, expected_repos, apache2_repos = fi


@parameterized_class([{
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test with fixtures and mock"""
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kargs):
            mock_resp = MagicMock()
            org_name = "google"
            org_url = f"https://api.github.com/orgs/{org_name}"
            repos_url = f"https://api.github.com/orgs/{org_name}/repos"
            if url == org_url:
                mock_resp.json.return_value = cls.org_payload
            elif url == repos_url:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = []
            return mock_resp
        mock_get.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns their names."""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filtering."""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
