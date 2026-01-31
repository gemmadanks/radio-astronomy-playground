"""Visualization module.

This module provides functions for plotting radio telescope
array configurations, sky models, uv-coverage, calibration solutions and images.

Functions:
    plot_telescope: Plot the array configuration of a telescope.
    plot_sky_model: Plot the sky model sources.
    plot_uv_coverage: Plot the UV coverage given UVW coordinates.
    plot_gains: Plot the calibration solutions.
    plot_image: Plot the 2D image data.
"""

from starbox.viz.plot import (
    plot_telescope,
    plot_gains,
    plot_sky_model,
    plot_uv_coverage,
    plot_image,
)

__all__ = [
    "plot_telescope",
    "plot_gains",
    "plot_sky_model",
    "plot_uv_coverage",
    "plot_image",
]
