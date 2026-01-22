"""Tests for predict module."""

from starbox.predict.predict import predict_visibilities


def test_predict_visibilities(small_telescope, skymodel, observation):
    """Test the predict_visibilities function."""
    expected_shape = (3, 45, 2)  # (num_times, num_baselines, num_channels)
    visibilities = predict_visibilities(small_telescope, skymodel, observation)
    assert visibilities.shape == expected_shape
