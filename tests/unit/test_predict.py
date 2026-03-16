"""Tests for predict module."""

import numpy as np

from starbox.constants import SPEED_OF_LIGHT
from starbox.geometry.lmn import calculate_lmn
from starbox.geometry.uvw import calculate_uvw
from starbox.config.skymodel import SkyModelConfig
from starbox.predict.predict import predict_visibilities
from starbox.simulate.skymodel import SkyModel


def test_predict_visibilities_returns_correct_shape(
    small_telescope, skymodel, observation
):
    """Test the predict_visibilities function returns correct shape."""
    expected_shape = (3, 45, 2)  # (num_times, num_baselines, num_channels)
    visibilities = predict_visibilities(small_telescope, skymodel, observation)
    assert visibilities.vis.shape == expected_shape


def test_predict_visibilities_has_consistent_uvw(small_telescope, observation):
    """UVW coordinates in output should match the geometry transform."""
    skymodel = SkyModel(
        SkyModelConfig(
            num_sources=1,
            max_flux_jy=1.0,
            field_centre_deg=(0.0, 0.0),
            fov_deg=1.0,
            seed=1,
        )
    )

    visibilities = predict_visibilities(small_telescope, skymodel, observation)
    expected_uvw_m = calculate_uvw(
        gmst_rad=observation.gmst_rad,
        phase_centre_rad=observation.phase_centre_rad,
        baselines_ecef_m=small_telescope.baselines_ecef,
    )

    np.testing.assert_allclose(visibilities.uvw_m, expected_uvw_m, atol=1e-12, rtol=0.0)


def test_predict_single_source_at_phase_centre_is_constant(
    small_telescope,
    observation,
):
    """A point source at phase centre should produce constant real visibilities."""
    flux_jy = 3.5
    phase_centre_ra_deg = observation.config.phase_center_ra
    phase_centre_dec_deg = observation.config.phase_center_dec

    skymodel = SkyModel(
        SkyModelConfig(
            num_sources=1,
            max_flux_jy=flux_jy,
            field_centre_deg=(phase_centre_ra_deg, phase_centre_dec_deg),
            fov_deg=1.0,
            seed=1,
        )
    )
    skymodel.ra_deg = np.array([phase_centre_ra_deg])
    skymodel.dec_deg = np.array([phase_centre_dec_deg])
    skymodel.flux_jy = np.array([flux_jy])

    visibilities = predict_visibilities(small_telescope, skymodel, observation)

    np.testing.assert_allclose(np.real(visibilities.vis), flux_jy, atol=1e-12, rtol=0.0)
    np.testing.assert_allclose(np.imag(visibilities.vis), 0.0, atol=1e-12, rtol=0.0)


def test_predict_single_offset_source_matches_geometric_phase(
    small_telescope,
    observation,
):
    """An offset source should follow the geometric delay phase law."""
    flux_jy = 2.0
    phase_centre_ra_deg = observation.config.phase_center_ra
    phase_centre_dec_deg = observation.config.phase_center_dec
    source_ra_deg = phase_centre_ra_deg + 0.2
    source_dec_deg = phase_centre_dec_deg

    skymodel = SkyModel(
        SkyModelConfig(
            num_sources=1,
            max_flux_jy=flux_jy,
            field_centre_deg=(phase_centre_ra_deg, phase_centre_dec_deg),
            fov_deg=1.0,
            seed=1,
        )
    )
    skymodel.ra_deg = np.array([source_ra_deg])
    skymodel.dec_deg = np.array([source_dec_deg])
    skymodel.flux_jy = np.array([flux_jy])

    visibilities = predict_visibilities(small_telescope, skymodel, observation)

    l_dir, m_dir, _ = calculate_lmn(
        ra_dec_rad=(np.deg2rad(source_ra_deg), np.deg2rad(source_dec_deg)),
        phase_centre_rad=observation.phase_centre_rad,
    )
    uvw_m = visibilities.uvw_m
    phase_cycles = (
        uvw_m[:, :, 0][:, :, np.newaxis] * l_dir
        + uvw_m[:, :, 1][:, :, np.newaxis] * m_dir
    ) * (observation.frequencies_hz / SPEED_OF_LIGHT)[np.newaxis, np.newaxis, :]
    expected_vis = flux_jy * np.exp(-2j * np.pi * phase_cycles)

    np.testing.assert_allclose(visibilities.vis, expected_vis, atol=1e-12, rtol=0.0)
    assert np.std(np.angle(visibilities.vis)) > 0.0
