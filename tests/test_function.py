"""Tests for syncspec function"""

import sys
from pathlib import Path
import json

# Add src directory to Python path for development
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

import pytest
from syncspec import syncspec

def test_syncspec_import():
    """Test that syncspec can be imported directly"""
    from syncspec import syncspec
    assert callable(syncspec)

import networkx as nx
from src.syncspec.function import syncspec

def test_syncspec():
    keyvalue = {}
    g, okv = syncspec(
        path="../syncspec-test/input/",
        output="../syncspec-test/output/",
        open_delimiter="{=",
        close_delimiter="=}",
        import_path="../syncspec-test/input/",
        keyvalue=keyvalue,
        log_file="syncspec.log"

    )
    nx.nx_pydot.write_dot(g, "syncspec.dot")

    # Convert dictionary to JSON and write to file
    with open("syncspec.json", "w", encoding="utf-8") as f:
        json.dump(okv, f, indent=2)