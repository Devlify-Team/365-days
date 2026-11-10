"""Example package logic to replace with your own public API."""


def greet(name: str = "world") -> str:
    """Return a greeting for a non-empty name."""
    if not isinstance(name, str):
        raise TypeError("name must be text")
    name = name.strip()
    if not name:
        raise ValueError("name must not be blank")
    return f"Hello, {name}!"
