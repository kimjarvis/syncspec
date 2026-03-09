import pytest
import json
from src.syncspec.fragment import Fragment
from src.syncspec.string import String
from src.syncspec.block import Block
from src.syncspec.error import Error
from src.syncspec.create_blocks_context import CreateBlocksContext
from src.syncspec.create_blocks import make_create_blocks


@pytest.mark.parametrize(
    "idx, top, txt, name, line, f_txt, f_line, exp_type, exp_ctx_top, exp_ctx_txt, exp_ctx_line, res_val",
    [
        (0, "", "", "mod", 0, "body", 10, String, "", "", 0, None),
        (1, "", "", "mod", 0, "dir", 20, type(None), "dir", "", 20, None),
        (2, "dir", "", "mod", 20, "mid", 30, type(None), "dir", "mid", 20, None),
        (3, '"key":', "val", "mod", 20, '"value"', 40, Block, '"key":', "val", 20, None),
    ]
)
def test_create_blocks_states(
        idx, top, txt, name, line, f_txt, f_line, exp_type,
        exp_ctx_top, exp_ctx_txt, exp_ctx_line, res_val
):
    ctx = CreateBlocksContext(idx, top, txt, line, name)
    func = make_create_blocks(ctx)
    res = func(Fragment(f_txt, f_line))

    assert (res is None) if exp_type is type(None) else isinstance(res, exp_type)
    assert (ctx.top_directive, ctx.text, ctx.line_number) == (exp_ctx_top, exp_ctx_txt, exp_ctx_line)

    if isinstance(res, Block):
        expected_combined = "{ " + top + " " + f_txt + " }"
        assert res.combined_directives == expected_combined
        assert res.directive == json.loads(expected_combined)


@pytest.mark.parametrize(
    "idx, top, txt, name, line, f_txt, f_line",
    [(3, "bad", "json", "mod", 20, "data", 40)]
)
def test_create_blocks_json_error(idx, top, txt, name, line, f_txt, f_line):
    ctx = CreateBlocksContext(idx, top, txt, line, name)
    func = make_create_blocks(ctx)
    res = func(Fragment(f_txt, f_line))

    assert isinstance(res, Error)
    assert res.name == name
    assert res.line_number == line
    assert "Invalid JSON" in res.message