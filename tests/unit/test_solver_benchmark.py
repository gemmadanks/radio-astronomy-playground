"""Benchmarks for the Solver.solve method.

Run with:
    pytest tests/unit/test_solver_benchmark.py --benchmark-only -v
"""

import numpy as np
import pytest

from starbox.calibrate.solver import Solver
from starbox.config.solver import SolverConfig
from starbox.visibility import VisibilitySet


def _make_solve_inputs(
    n_timesteps: int,
    n_stations: int,
    n_channels: int,
    *,
    rng: np.random.Generator,
) -> tuple:
    """Build (solver, observed, model, n_stations) with realistic gains applied.

    The observed visibilities are model * known station phase gains so the
    optimizer converges to a well-defined minimum, giving meaningful timings.
    """
    station_pairs = [
        (i, j) for i in range(n_stations) for j in range(i + 1, n_stations)
    ]
    n_baselines = len(station_pairs)
    station1 = np.array([p[0] for p in station_pairs], dtype=np.int32)
    station2 = np.array([p[1] for p in station_pairs], dtype=np.int32)

    # Smooth model visibilities (unit amplitude, varying phase)
    model_vis = np.exp(
        1j * rng.uniform(-np.pi, np.pi, (n_timesteps, n_baselines, n_channels))
    ).astype(np.complex128)

    # Known station gains: station 0 is the reference (phase = 0)
    station_phases = np.zeros(n_stations)
    station_phases[1:] = rng.uniform(-np.pi / 4, np.pi / 4, n_stations - 1)
    gains = np.exp(1j * station_phases)

    # Apply gains: V_ij = g_i * conj(g_j) * M_ij
    gain_1 = gains[station1][np.newaxis, :, np.newaxis]
    gain_2 = gains[station2][np.newaxis, :, np.newaxis]
    observed_vis = gain_1 * np.conj(gain_2) * model_vis

    time_grid = np.linspace(59000.0, 59000.0 + n_timesteps / 86400, n_timesteps)
    freq_grid = np.linspace(1e8, 2e8, n_channels)
    weights = np.ones((n_timesteps, n_baselines, n_channels))

    model = VisibilitySet(
        vis=model_vis,
        uvw_m=np.zeros((n_timesteps, n_baselines, 3)),
        station1=station1,
        station2=station2,
        times_mjd=time_grid,
        freqs_hz=freq_grid,
        weights=weights,
    )
    observed = VisibilitySet(
        vis=observed_vis,
        uvw_m=np.zeros((n_timesteps, n_baselines, 3)),
        station1=station1,
        station2=station2,
        times_mjd=time_grid,
        freqs_hz=freq_grid,
        weights=weights,
    )
    # Single solution bin so optimizer has fewest parameters to solve
    solver = Solver(SolverConfig(solution_interval_seconds=float(n_timesteps)))
    return solver, observed, model, n_stations


SCENARIOS = {
    "small  ( 3t /  4s /  2ch)": dict(n_timesteps=3, n_stations=4, n_channels=2),
    "medium (10t /  8s /  4ch)": dict(n_timesteps=10, n_stations=8, n_channels=4),
}


@pytest.fixture(params=list(SCENARIOS.keys()))
def solve_inputs(request):
    """Parametrized fixture returning (solver, observed, model, n_stations)."""
    scenario = SCENARIOS[request.param]
    rng = np.random.default_rng(42)
    return _make_solve_inputs(rng=rng, **scenario)


@pytest.mark.benchmark(min_rounds=3, max_time=30.0, warmup=False)
def test_solver_solve_benchmark(benchmark, solve_inputs):
    """Benchmark Solver.solve across small, medium, and large observation sizes."""
    solver, observed, model, n_stations = solve_inputs

    result = benchmark(solver.solve, observed, model, n_stations)

    # Smoke-check: output has the right shape and unit modulus
    assert result.station_phase_gains.ndim == 3
    assert np.allclose(np.abs(result.station_phase_gains), 1.0, atol=1e-4)
