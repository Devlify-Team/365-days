import math

import pytest

from reading_stats import summarize


@pytest.fixture
def readings():
    return [10.0, 12.5, 17.5]


def test_summary_from_fixture(readings):
    result = summarize(readings)
    assert result["count"] == 3
    assert result["minimum"] == 10.0
    assert result["maximum"] == 17.5
    assert result["mean"] == pytest.approx(40 / 3)


@pytest.mark.parametrize(
    ("values", "minimum", "maximum", "mean"),
    [([5], 5, 5, 5.0), ([-2, 4], -2, 4, 1.0)],
)
def test_small_input_cases(values, minimum, maximum, mean):
    result = summarize(values)
    assert result["minimum"] == minimum
    assert result["maximum"] == maximum
    assert result["mean"] == pytest.approx(mean)


def test_empty_input_is_rejected():
    with pytest.raises(ValueError, match="at least one"):
        summarize([])


@pytest.mark.parametrize("bad_value", [True, "12", None])
def test_non_numeric_values_are_rejected(bad_value):
    with pytest.raises(TypeError, match="integers or floats"):
        summarize([bad_value])


@pytest.mark.parametrize("bad_value", [math.inf, -math.inf, math.nan])
def test_non_finite_values_are_rejected(bad_value):
    with pytest.raises(ValueError, match="finite"):
        summarize([bad_value])
