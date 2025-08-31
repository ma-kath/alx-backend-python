#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map function."""

import unittest
from unittest.mock import Mock, patch
 
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize

class TestAccessNestedMap(unittest.TestCase):
    """Test case for utils.access_nested_map function."""
    
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map,path: tuple, expected):
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple):
        """Test that access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(cm.exception.args[0], path[-1])
        

class TestGetJson(unittest.TestCase):
    """Test case for utils.get_json function."""
    
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url: str, test_playload: dict, mock_get: Mock):
        """Test that get_json returns expected payload and calls requests.get once."""
        mock_get.return_value.json.return_value = test_playload
        
        result = get_json(test_url)
        
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_playload)
    
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
        
        with patch.object(test_obj, 'a_method', wraps=test_obj.a_method) as mock_method:
            result1 = test_obj.a_property
            result2 = test_obj.a_property
            
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()