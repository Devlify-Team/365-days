import pytest

from python_template import greet


def test_default_greeting():
    assert greet() == "Hello, world!"


@pytest.mark.parametrize("name", ["Ada", "  Lin  "])
def test_named_greeting(name):
    assert greet(name).startswith("Hello, ")


def test_rejects_blank_name():
    with pytest.raises(ValueError, match="must not be blank"):
        greet("  ")


def test_rejects_non_text_name():
    with pytest.raises(TypeError, match="must be text"):
        greet(None)
