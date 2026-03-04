import pytest
from src.syncspec.parse_into_fragments import Fragment
from src.syncspec.fragments_to_blocks import (
    fragments_to_tracker,
    reset_tracker_manager,
    Tracker,
)


@pytest.fixture(autouse=True)
def reset_state():
    reset_tracker_manager()


@pytest.mark.parametrize("texts, expected_index, expected_line, expected_stack_len", [
    ([""], 0, 1, 1),
    (["", ""], 1, 1, 2),
    (["\n"], 0, 2, 1),
    (["a", "b\n"], 1, 2, 2),
])
def test_cumulative_state(texts, expected_index, expected_line, expected_stack_len):
    tracker = None
    for text in texts:
        fragment = Fragment(text=text, name="test", open_delimiter="{", close_delimiter="}")
        tracker = fragments_to_tracker(fragment)

    # Verify cumulative state after all fragments are processed
    assert tracker is not None
    assert tracker.index == expected_index
    assert tracker.line == expected_line
    assert len(tracker.stack) == expected_stack_len
    assert tracker.name == "test"