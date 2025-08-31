#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map function."""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""
    def test_memoize(self):
        """Test that memoize caches the result of a method call."""
        class TestClass:
            """Test class with a memoized property."""
            def a_method(self) -> int:
                """Test class with a memoized property."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()
        test_obj = TestClass()
        with patch.object(
            test_obj,
            'a_method',
            wraps=test_obj.a_method
        ) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()
