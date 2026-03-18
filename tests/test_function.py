"""Tests for syncspec function"""

import sys
from pathlib import Path

# Add src directory to Python path for development
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from syncspec import syncspec

def test_syncspec_import():
    """Test that syncspec can be imported directly"""
    from syncspec import syncspec
    assert callable(syncspec)

def test_syncspec_function():
    """Test the syncspec function"""
    result = syncspec()
    assert result is not None
    # Add more specific tests based on your function's behavior