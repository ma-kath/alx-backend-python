#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map function."""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestGetJson(unittest.TestCase):
    """Test case for utils.get_json function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(
        self,
        test_url: str,
        test_playload: dict,
        mock_get: Mock
    ):
        """get_json returns expected payload and calls requests.get once."""
        mock_get.return_value.json.return_value = test_playload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_playload)
