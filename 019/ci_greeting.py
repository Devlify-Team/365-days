"""Small example module exercised by the Day 019 GitHub Actions workflow."""


def greet(name="world"):
    """Return a greeting for a non-blank text name."""
    if not isinstance(name, str):
        raise TypeError("name must be text")
    name = name.strip()
    if not name:
        raise ValueError("name must not be blank")
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet())
