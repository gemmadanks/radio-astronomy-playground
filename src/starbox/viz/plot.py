"""Functions for plotting data."""

import plotly.express as px
from starbox.calibrate.solutions import Solutions
from starbox.simulate.skymodel import SkyModel
from plotly.graph_objects import Figure
from starbox.simulate.telescope import Telescope
import numpy as np


def uv_coverage(uvw_coordinates: np.ndarray, title: str = "UV Coverage") -> Figure:
    """Plot the UV coverage given UVW coordinates."""

    u = uvw_coordinates[:, 0]
    v = uvw_coordinates[:, 1]

    fig = px.scatter(
        x=u, y=v, title=title, labels={"x": "U (wavelengths)", "y": "V (wavelengths)"}
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    return fig


def sky_model(sky_model: SkyModel) -> Figure:
    """Plot the sky model sources."""
    ras, decs, fluxes = sky_model.as_arrays()
    fig = px.scatter(
        x=ras,
        y=decs,
        size=fluxes,
        title="Sky Model",
        labels={"x": "Right Ascension (deg)", "y": "Declination (deg)"},
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def array_configuration(telescope: Telescope, title=None):
    """Plot the array configuration given antenna coordinates."""
    if title is None:
        plot_title = f"Telescope Array Configuration: {telescope.name}"
    else:
        plot_title = title
    fig = px.scatter(
        x=telescope.array[:, 0],
        y=telescope.array[:, 1],
        title=plot_title,
    )
    fig.update_layout(
        xaxis_title="X (North) [m]",
        yaxis_title="Y (East) [m]",
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
    )
    fig.update_traces(marker=dict(size=15, color="blue", symbol="cross"))

    return fig


def gains(gains: Solutions) -> Figure:
    """Plot the calibration solutions."""

    fig = px.imshow(
        gains.gains[:, :, 0].real.T,
        title="Gains",
        labels={
            "x": "time",
            "y": "frequency",
        },
        origin="lower",
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def image(image: np.ndarray, title="Imaged Sky") -> Figure:
    """Plot the image."""

    fig = px.imshow(image, title=title, labels={"x": "RA", "y": "Dec"})
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig
