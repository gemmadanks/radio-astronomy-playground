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


def plot_gains(solutions: Solutions, station_index: int = 0) -> Figure:
    """Plot the gain phase for a single station.

    Rendering one station at a time keeps the figure payload small enough for
    notebook frontends such as marimo.
    """

    n_stations = solutions.station_phase_gains.shape[2]
    station_index = int(np.clip(station_index, 0, n_stations - 1))
    phase_deg = np.angle(solutions.station_phase_gains[:, :, station_index], deg=True)
    fig = px.imshow(
        phase_deg.T,
        title=f"Gain Phase: Station {station_index}",
        labels={
            "x": "time",
            "y": "frequency",
            "color": "phase (deg)",
        },
        origin="lower",
        aspect="auto",
    )
    return fig


def plot_image(
    image: np.ndarray,
    title: str = "Imaged Sky",
    fov_deg: float | None = None,
    height: int = 350,
    zmin: float | None = None,
    zmax: float | None = None,
    color_continuous_scale: str | list[str] | None = None,
) -> Figure:
    """Plot the image."""

    if fov_deg is None:
        fig = px.imshow(
            image,
            origin="lower",
            title=title,
            labels={"x": "RA", "y": "Dec"},
            zmin=zmin,
            zmax=zmax,
            color_continuous_scale=color_continuous_scale,
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
            zmin=zmin,
            zmax=zmax,
            color_continuous_scale=color_continuous_scale,
        )
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=40, b=10))
    fig.update_yaxes(scaleanchor=None)
    return fig
