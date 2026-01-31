"""Tests for functions that build corruptions."""

from starbox.factory.corruptions import build_corruptions
from starbox.simulate.corruptions import Corruptions


def test_build_corruptions_returns_corruptions(corruptions_config):
    """Test that build_corruptions returns a Corruptions instance."""
    corruptions = build_corruptions(corruptions_config)

    assert isinstance(corruptions, Corruptions)
    assert corruptions.config.rms_noise == corruptions_config.rms_noise
    assert corruptions.config.rms_phase_gain == corruptions_config.rms_phase_gain
