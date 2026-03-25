"""Functions for plotting data."""

import plotly.express as px
from starbox.calibrate.solutions import Solutions
from starbox.simulate.skymodel import SkyModel
from plotly.graph_objects import Figure
from starbox.simulate.telescope import Telescope
import numpy as np


def plot_uv_coverage(uvw_coordinates: np.ndarray, title: str = "UV Coverage") -> Figure:
    """Plot the UV coverage given UVW coordinates.

    Args:
        uvw_coordinates:
            - (T, B, 3): T timesteps, B baselines, 3 coordinates
        title: Plot title.

    Averages UV coordinates across time to show unique baseline coverage.
    """
    uvw_coordinates = np.mean(uvw_coordinates, axis=0)  # (B, 3)

    u = uvw_coordinates[:, 0]
    v = uvw_coordinates[:, 1]

    fig = px.scatter(
        x=u, y=v, title=title, labels={"x": "U (wavelengths)", "y": "V (wavelengths)"}
    )
    fig.update_layout(width=500, height=500)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def plot_sky_model(sky_model: SkyModel) -> Figure:
    """Plot the sky model sources."""
    ras, decs, fluxes = sky_model.as_arrays()
    plot_range = max(np.max(np.abs(ras)), np.max(np.abs(decs))) * 1.2
    fig = px.scatter(
        x=ras,
        y=decs,
        size=fluxes,
        title="Sky Model",
        labels={"x": "Right Ascension (deg)", "y": "Declination (deg)"},
    )
    fig.update_layout(width=500, height=500)
    fig.update_yaxes(scaleanchor="x", scaleratio=1, range=[-plot_range, plot_range])
    fig.update_xaxes(range=[-plot_range, plot_range])
    return fig


def plot_telescope(telescope: Telescope) -> Figure:
    """Plot the array configuration given antenna coordinates."""
    fig = px.scatter(
        x=telescope.station_positions[:, 0],
        y=telescope.station_positions[:, 1],
        title=f"{telescope.name}",
    )
    fig.update_layout(
        xaxis_title="East [m]",
        yaxis_title="North [m]",
        yaxis_scaleanchor="x",
        yaxis_scaleratio=1,
    )
    fig.update_traces(marker=dict(size=15, color="blue", symbol="cross"))

    return fig


def plot_gains(solutions: Solutions) -> Figure:
    """Plot the calibration solutions."""

    fig = px.imshow(
        # Transpose from (time, freq, station) to (station, freq, time) so each frame has
        # time on the x-axis, frequency on the y-axis, and animation_frame=0 animates stations.
        np.real(np.transpose(solutions.station_phase_gains, (2, 1, 0))),
        title="Gains",
        labels={
            "x": "time",
            "y": "frequency",
        },
        origin="lower",
        aspect="auto",
        animation_frame=0,  # Animate over stations
    )
    return fig


def plot_image(
    image: np.ndarray, title: str = "Imaged Sky", fov_deg: float | None = None
) -> Figure:
    """Plot the image."""

    if fov_deg is None:
        fig = px.imshow(
            image,
            origin="lower",
            title=title,
            labels={"x": "RA", "y": "Dec"},
        )
    else:
        x_deg = np.linspace(-fov_deg / 2.0, fov_deg / 2.0, image.shape[1])
        y_deg = np.linspace(-fov_deg / 2.0, fov_deg / 2.0, image.shape[0])
        fig = px.imshow(
            image,
            x=x_deg,
            y=y_deg,
            origin="lower",
            title=title,
            labels={"x": "ΔRA (deg)", "y": "ΔDec (deg)"},
        )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig
