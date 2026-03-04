from dataclasses import dataclass
from src.syncspec.parse_into_fragments import Fragment


@dataclass
class Tracker:
    stack: list[str]
    index: int
    name: str
    open_delimiter: str
    close_delimiter: str
    line: int


class TrackerManager:
    def __init__(self):
        self.stack: list[str] = []
        self.index: int = 0
        self.line: int = 1  # Initialise to 1 as per specification

    def reset(self):
        self.stack = []
        self.index = 0
        self.line = 1


_manager = TrackerManager()


def fragments_to_tracker(fragment: Fragment) -> Tracker:
    # Update accumulators
    _manager.line += fragment.text.count('\n')
    _manager.stack.append(fragment.text)

    # Capture state for Tracker (Index is 0-based call number)
    current_index = _manager.index
    _manager.index += 1

    return Tracker(
        stack=list(_manager.stack),  # Make a copy of the stack
        index=current_index,
        name=fragment.name,
        open_delimiter=fragment.open_delimiter,
        close_delimiter=fragment.close_delimiter,
        line=_manager.line
    )


def reset_tracker_manager():
    _manager.reset()