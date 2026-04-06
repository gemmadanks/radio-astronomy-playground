"""Functions for plotting data."""

import numpy as np
import plotly.express as px
from plotly.graph_objects import Figure
import plotly.graph_objects as go
from starbox.calibrate.solutions import Solutions
from starbox.simulate.skymodel import SkyModel
from starbox.simulate.telescope import Telescope


def plot_uv_coverage(
    uvw_coordinates: np.ndarray,
    freqs_hz: np.ndarray,
    title: str = "UV Coverage",
    max_timesteps: int = 10,
) -> Figure:
    """Plot UV coverage points in wavelength units.

    Args:
        uvw_coordinates:
            - (T, B, 3): T timesteps, B baselines, 3 coordinates in meters
        freqs_hz: Channel frequencies in Hz used to convert UV coordinates from
            meters to wavelengths using the mean frequency.
        title: Plot title.
        max_timesteps: Maximum number of timesteps to plot. If the input has more
            timesteps, they will be downsampled evenly across time.

    Shows all UV sample points (positive and mirrored conjugates) colored by time.
    Downsamples in time if necessary to keep the Plotly payload manageable.
    """
    uvw = np.asarray(uvw_coordinates, dtype=np.float64)
    if uvw.ndim != 3 or uvw.shape[2] != 3:
        msg = "uvw_coordinates must have shape (time, baseline, 3)"
        raise ValueError(msg)

    # Downsample in time if needed
    n_timesteps_orig = uvw.shape[0]
    if n_timesteps_orig > max_timesteps:
        indices = np.linspace(0, n_timesteps_orig - 1, max_timesteps, dtype=int)
        uvw = uvw[indices, :, :]
        n_timesteps = len(indices)
    else:
        n_timesteps = n_timesteps_orig

    freqs = np.asarray(freqs_hz, dtype=np.float64)
    if freqs.size == 0:
        msg = "freqs_hz must be a non-empty array of finite positive frequencies in Hz"
        raise ValueError(msg)
    if not np.all(np.isfinite(freqs)):
        msg = "freqs_hz must contain only finite frequencies in Hz"
        raise ValueError(msg)
    if np.any(freqs <= 0):
        msg = "freqs_hz must contain only positive frequencies in Hz"
        raise ValueError(msg)

    ref_freq_hz = float(np.mean(freqs))
    wavelength_m = 299_792_458.0 / ref_freq_hz
    u = uvw[:, :, 0] / wavelength_m  # (T, B)
    v = uvw[:, :, 1] / wavelength_m  # (T, B)

    n_baselines = u.shape[1]

    # Build grey line segments: for each baseline connect points across time,
    # then the mirrored track, separated by None to break the line between groups
    line_x: list = []
    line_y: list = []
    for b in range(n_baselines):
        line_x.extend(u[:, b].tolist())
        line_x.append(None)
        line_x.extend((-u[:, b]).tolist())
        line_x.append(None)
        line_y.extend(v[:, b].tolist())
        line_y.append(None)
        line_y.extend((-v[:, b]).tolist())
        line_y.append(None)

    # All points (positive + mirrored) colored by time
    time_grid = np.broadcast_to(
        np.arange(n_timesteps, dtype=np.float64)[:, np.newaxis], u.shape
    )
    u_all = np.concatenate([u, -u]).ravel()
    v_all = np.concatenate([v, -v]).ravel()
    time_all = np.concatenate([time_grid, time_grid]).ravel()

    fig = go.Figure()

    # Grey lines connecting timesteps for each baseline
    fig.add_trace(
        go.Scattergl(
            x=line_x,
            y=line_y,
            mode="lines",
            line=dict(color="rgba(150, 150, 150, 0.5)", width=1),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # Markers colored by time
    fig.add_trace(
        go.Scattergl(
            x=u_all,
            y=v_all,
            mode="markers",
            marker=dict(
                size=3,
                color=time_all,
                colorscale="Viridis",
                cmin=0,
                cmax=max(n_timesteps - 1, 1),
                colorbar=dict(title="Time step"),
            ),
            hovertemplate="U: %{x:.2f}<br>V: %{y:.2f}<extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="U (wavelengths)",
        yaxis_title="V (wavelengths)",
        width=500,
        height=500,
        hovermode="closest",
    )
    fig.update_xaxes(
        zeroline=True, zerolinewidth=1, zerolinecolor="rgba(0, 0, 0, 0.25)"
    )
    fig.update_yaxes(
        zeroline=True, zerolinewidth=1, zerolinecolor="rgba(0, 0, 0, 0.25)"
    )
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
