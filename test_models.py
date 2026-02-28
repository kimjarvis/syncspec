import pytest
from models import B, C, D, E

def test_b_execute(capsys):
    b = B(t='b', b_field="test")
    b.execute()
    assert capsys.readouterr().out == "B: test\n"

def test_c_execute(capsys):
    c = C(t='c', c_field=42)
    c.execute()
    assert capsys.readouterr().out == "C: 42\n"

def test_e_execute(capsys):
    e = E(d=[
        D(x={'t': 'b', 'b_field': 'hello'}),
        D(x={'t': 'c', 'c_field': 10})
    ])
    e.execute()
    out = capsys.readouterr().out
    assert "B: hello\n" in out
    assert "C: 10\n" in out

def test_invalid_discriminator():
    with pytest.raises(Exception):
        D(x={'t': 'invalid', 'b_field': 'x'})