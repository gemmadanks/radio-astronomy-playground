"""Fixtures for tests."""

import pytest
from starbox.simulate.telescope import Telescope
import plotly.io as pio


@pytest.fixture(scope="session", autouse=True)
def configure_plotly_for_tests():
    """Configure Plotly to not open browser during tests."""
    # Set renderer to 'json' or 'png' instead of 'browser'
    pio.renderers.default = "json"


@pytest.fixture
def small_telescope():
    """A simple telescope model for a small array."""
    return Telescope(name="SmallArray", num_antennas=10, diameter=20.0)
