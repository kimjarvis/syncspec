import pytest
from src.syncspec.text import Text
from src.syncspec.fragment import Fragment
from src.syncspec.error import Error
from src.syncspec.monad import Monad
from src.syncspec.validate_text import validate_text

@pytest.fixture(autouse=True)
def reset_monad():
    Monad.state.clear()
    Monad.state["open_delimiter"] = "{{"
    Monad.state["close_delimiter"] = "}}"
    Monad.state["name"] = "test"
    Monad.state["length"] = 1
    Monad.state["index"] = 0
    yield

@pytest.mark.parametrize("content, expected_type", [
    ("", Fragment),
    ("Hello World", Fragment),
    ("{{A}}B{{C}}", Fragment),
    ("{{A}}", Error),
    ("{{A{{B}}C}}", Error),
    ("}}A{{", Error),
    ("{{A}}B{{C}}D{{E}}", Error), # 3 pairs
])
def test_validate_text_cases(content, expected_type):
    result = validate_text(Text(text=content))
    assert isinstance(result, expected_type)

def test_monad_state_validation():
    Monad.state["index"] = 5
    Monad.state["length"] = 5
    result = validate_text(Text(text=""))
    assert isinstance(result, Error)
    assert "Invalid index" in result.message

def test_delimiter_validation():
    Monad.state["open_delimiter"] = "{{"
    Monad.state["close_delimiter"] = "{{"
    result = validate_text(Text(text=""))
    assert isinstance(result, Error)
    assert "distinct" in result.message