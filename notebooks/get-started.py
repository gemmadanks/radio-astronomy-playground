import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import logging
    import numpy as np

    from starbox import Imager
    from starbox.config import (
        SkyModelConfig,
        ObservationConfig,
        TelescopeConfig,
        TelescopeSiteConfig,
        CorruptionsConfig,
        SolverConfig,
        ExperimentConfig,
    )
    from starbox.factory import (
        build_skymodel,
        build_observation,
        build_telescope,
        build_corruptions,
        build_solver,
    )
    from starbox.viz import plot
    from starbox.predict.predict import predict_visibilities, generate_psf_visibilities
    from starbox.io.save import save

    return (
        CorruptionsConfig,
        ExperimentConfig,
        Imager,
        ObservationConfig,
        SkyModelConfig,
        SolverConfig,
        TelescopeConfig,
        TelescopeSiteConfig,
        build_corruptions,
        build_observation,
        build_skymodel,
        build_solver,
        build_telescope,
        generate_psf_visibilities,
        logging,
        mo,
        np,
        plot,
        predict_visibilities,
        save,
    )


@app.cell
def _():
    seed = 42
    return (seed,)


@app.cell
def _(logging):
    logging.basicConfig(level=logging.INFO)
    return


@app.cell
def _(mo):
    mo.md(r"""
    /// attention | Warning!

    This is a work in progress.
    ///
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # ✨ Welcome to [Radio Astronomy Playground](https://open-research.gemmadanks.com/radio-astronomy-playground/)! ✨
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    This is an interactive experiment for learning how a radio interferometer measures the radio brightness of sources in the sky and how to calibrate for phase-only gains and generate high quality images.

    Configure your experiment below and see how the final image changes.

    Alternatively, if you have a configuration file you can load it below.

    More details on the steps involved are given below the results.
    """)
    return


@app.cell
def _(mo):
    file_browser = mo.ui.file_browser(
        multiple=False,
        initial_path="config/",
        filetypes=["json"],
        restrict_navigation=False,
    )
    file_browser  # pyright: ignore[reportUnusedExpression]
    return (file_browser,)


@app.cell
def _(mo):
    # Sky model
    num_sources_slider = mo.ui.slider(1, 10, value=1, label="Number of point sources: ")
    max_flux_slider = mo.ui.slider(
        1, 10, value=10, label="Maximum source brightness (Jy): "
    )
    fov_slider = mo.ui.slider(
        1.0, 10.0, step=0.1, value=1.0, label="Field of view (degrees): "
    )

    # Telescope
    num_stations_slider = mo.ui.slider(2, 100, value=68, label="Number of stations: ")
    telescope_diameter_slider = mo.ui.slider(
        1, 100, value=20, label="Maximum diameter of telescope (km): "
    )

    # Observation
    start_time_mjd_slider = mo.ui.slider(
        59000, 69000, value=68356, label="Start time (MJD): "
    )
    observation_length_slider = mo.ui.slider(
        1, 24, value=4, label="Observation length (hrs): "
    )
    num_timesteps_slider = mo.ui.slider(
        1, 24 * 60, value=4 * 60, label="Number of timesteps: "
    )
    start_freq_slider = mo.ui.slider(
        100, 1000, value=100, label="Mid-point frequency of first channel (MHz): "
    )
    num_channels_slider = mo.ui.slider(1, 100, value=32, label="Number of channels: ")
    bandwidth_slider = mo.ui.slider(
        1, 100, value=32, label="Total frequency bandwidth (MHz): "
    )
    phase_centre_dec_slider = mo.ui.slider(
        -90, 90, value=0, label="Phase center declination (deg): "
    )

    # Corruptions
    phase_rms_slider = mo.ui.slider(
        0, 30, value=10, label="Per-station phase gain RMS (degrees): "
    )
    phase_time_corr_slider = mo.ui.slider(
        0.0, 0.999, step=0.01, value=0.95, label="Phase time correlation: "
    )
    phase_freq_corr_slider = mo.ui.slider(
        0.0, 0.999, step=0.01, value=0.85, label="Phase frequency correlation: "
    )
    noise_rms_slider = mo.ui.slider(0.0, 100.0, step=1, value=0.0, label="Noise RMS: ")

    # Calibration
    solution_interval_seconds_slider = mo.ui.slider(
        1, 600, value=300, label="Solution interval (s): "
    )
    solution_interval_hz_slider = mo.ui.slider(
        1, 100, value=4, label="Solution interval (MHz): "
    )
    return (
        bandwidth_slider,
        fov_slider,
        max_flux_slider,
        noise_rms_slider,
        num_channels_slider,
        num_sources_slider,
        num_stations_slider,
        num_timesteps_slider,
        observation_length_slider,
        phase_centre_dec_slider,
        phase_freq_corr_slider,
        phase_rms_slider,
        phase_time_corr_slider,
        solution_interval_hz_slider,
        solution_interval_seconds_slider,
        start_freq_slider,
        start_time_mjd_slider,
        telescope_diameter_slider,
    )


@app.cell
def _(mo, num_stations_slider):
    # Plotting
    gain_station_dropdown = mo.ui.dropdown(
        options=list(range(num_stations_slider.value)),
        value=1,
        label="Station number: ",
    )
    return (gain_station_dropdown,)


@app.cell
def _(file_browser):
    file_browser.path(index=0)
    return


@app.cell
def _(
    SkyModelConfig,
    build_skymodel,
    fov_slider,
    max_flux_slider,
    mo,
    num_sources_slider,
    plot,
    seed,
):
    sky_model_config = SkyModelConfig(
        num_sources=num_sources_slider.value,
        max_flux_jy=max_flux_slider.value,
        fov_deg=fov_slider.value,
        field_centre_deg=(0, 0),
        seed=seed,
    )
    sky_model = build_skymodel(sky_model_config)
    sky_model_fig = mo.ui.plotly(plot.plot_sky_model(sky_model))
    return sky_model, sky_model_config, sky_model_fig


@app.cell
def _(
    TelescopeConfig,
    TelescopeSiteConfig,
    build_telescope,
    mo,
    num_stations_slider,
    plot,
    seed,
    telescope_diameter_slider,
):
    telescope_site = TelescopeSiteConfig(
        latitude_deg=0.0, longitude_deg=0.0, altitude_m=0.0
    )
    telescope_config = TelescopeConfig(
        num_stations=num_stations_slider.value,
        diameter=telescope_diameter_slider.value * 1000,
        seed=seed,
        site=telescope_site,
    )
    telescope = build_telescope(telescope_config)
    telescope_fig = mo.ui.plotly(plot.plot_telescope(telescope))
    return telescope, telescope_config, telescope_fig


@app.cell
def _(
    fov_slider,
    max_flux_slider,
    mo,
    num_sources_slider,
    num_stations_slider,
    sky_model_fig,
    telescope_diameter_slider,
    telescope_fig,
):
    mo.hstack(
        [
            mo.vstack(
                [sky_model_fig, num_sources_slider, max_flux_slider, fov_slider],
                justify="start",
            ),
            mo.vstack(
                [telescope_fig, num_stations_slider, telescope_diameter_slider],
                justify="start",
            ),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Observation
    """)
    return


@app.cell
def _(
    bandwidth_slider,
    mo,
    num_channels_slider,
    num_timesteps_slider,
    observation_length_slider,
    phase_centre_dec_slider,
    start_freq_slider,
    start_time_mjd_slider,
):
    mo.vstack(
        [
            mo.hstack(
                [
                    start_time_mjd_slider,
                    observation_length_slider,
                    num_timesteps_slider,
                ],
                justify="start",
            ),
            mo.hstack(
                [start_freq_slider, num_channels_slider, bandwidth_slider],
                justify="start",
            ),
            mo.hstack(
                [phase_centre_dec_slider],
                justify="start",
            ),
        ]
    )
    return


@app.cell
def _(
    ObservationConfig,
    bandwidth_slider,
    build_observation,
    num_channels_slider,
    num_timesteps_slider,
    observation_length_slider,
    phase_centre_dec_slider,
    start_freq_slider,
    start_time_mjd_slider,
):
    observation_config = ObservationConfig(
        start_time_mjd=start_time_mjd_slider.value,
        observation_length=observation_length_slider.value * 3600,
        num_timesteps=num_timesteps_slider.value,
        start_frequency=start_freq_slider.value * 1e6,
        num_channels=num_channels_slider.value,
        total_bandwidth=bandwidth_slider.value * 1e6,
        phase_centre_dec=phase_centre_dec_slider.value,
    )
    observation = build_observation(observation_config)
    return observation, observation_config


@app.cell
def _(mo):
    mo.md(r"""
    ### Corruptions
    """)
    return


@app.cell
def _(
    CorruptionsConfig,
    build_corruptions,
    noise_rms_slider,
    phase_freq_corr_slider,
    phase_rms_slider,
    phase_time_corr_slider,
    seed,
):
    corruptions_config = CorruptionsConfig(
        rms_noise=noise_rms_slider.value,
        rms_phase_gain=phase_rms_slider.value,
        phase_time_correlation=phase_time_corr_slider.value,
        phase_frequency_correlation=phase_freq_corr_slider.value,
        seed=seed,
    )
    corruptions = build_corruptions(corruptions_config)
    return corruptions, corruptions_config


@app.cell
def _(
    SolverConfig,
    build_solver,
    solution_interval_hz_slider,
    solution_interval_seconds_slider,
):
    solver_config = SolverConfig(
        solution_interval_seconds=solution_interval_seconds_slider.value,
        solution_interval_hz=solution_interval_hz_slider.value * 1e6,
    )
    solver = build_solver(solver_config)
    return solver, solver_config


@app.cell
def _(Imager, fov_slider):
    imager = Imager(fov_deg=fov_slider.value, grid_size=256)
    return (imager,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Results
    """)
    return


@app.cell(hide_code=True)
def _(fov_slider, imager, mo):
    pixels_per_degree = imager.grid_size / max(fov_slider.value, 1e-12)
    degrees_per_pixel = fov_slider.value / imager.grid_size
    mo.md(
        f"""
        **Image sampling**

        - Field of view: **{fov_slider.value:.2f}°**
        - Image size: **{imager.grid_size} × {imager.grid_size}** pixels
        - Pixel scale: **{degrees_per_pixel:.5f}°/pixel**
        - Sampling density: **{pixels_per_degree:.2f} pixels/degree**
        """
    )
    return


@app.cell
def _(sky_model):
    sky_model.config
    return


@app.cell
def _(
    generate_psf_visibilities,
    imager,
    observation,
    predict_visibilities,
    sky_model,
    telescope,
):
    model_visibilities = predict_visibilities(telescope, sky_model, observation)
    psf_visibilities = generate_psf_visibilities(model_visibilities)
    psf_image = imager.image(psf_visibilities)
    return model_visibilities, psf_image


@app.cell
def _(fov_slider, mo, model_visibilities, plot, psf_image):
    mo.hstack(
        [
            plot.plot_uv_coverage(
                model_visibilities.uvw_m,
                freqs_hz=model_visibilities.freqs_hz,
            ),
            plot.plot_image(psf_image, title="PSF", fov_deg=fov_slider.value),
        ],
        gap="1rem",  # Reduce spacing between plots
        widths=["50%", "50%"],  # Equal width columns
    )
    return


@app.cell
def _(corruptions, model_visibilities, num_stations_slider, solver):
    observed_visibilities = corruptions.apply(model_visibilities)
    gains = solver.solve(
        observed_visibilities, model_visibilities, num_stations_slider.value
    )
    corrected_visibilities = gains.apply(observed_visibilities)
    return corrected_visibilities, gains, observed_visibilities


@app.cell
def _(
    corrected_visibilities,
    imager,
    model_visibilities,
    observed_visibilities,
):
    dirty_image = imager.image(observed_visibilities)
    corrected_image = imager.image(corrected_visibilities)
    model_image = imager.image(model_visibilities)
    dirty_residual_image = dirty_image - model_image
    calibrated_residual_image = corrected_image - model_image
    return (
        calibrated_residual_image,
        corrected_image,
        dirty_image,
        dirty_residual_image,
        model_image,
    )


@app.cell
def _(
    mo,
    noise_rms_slider,
    phase_freq_corr_slider,
    phase_rms_slider,
    phase_time_corr_slider,
    solution_interval_hz_slider,
    solution_interval_seconds_slider,
):
    mo.vstack(
        [
            mo.hstack([noise_rms_slider, phase_rms_slider], justify="start"),
            mo.hstack(
                [phase_time_corr_slider, phase_freq_corr_slider], justify="start"
            ),
            mo.hstack(
                [solution_interval_seconds_slider, solution_interval_hz_slider],
                justify="start",
            ),
        ],
        justify="start",
    )
    return


@app.cell
def _(
    calibrated_residual_image,
    corrected_image,
    dirty_image,
    dirty_residual_image,
    fov_slider,
    gain_station_dropdown,
    gains,
    mo,
    model_image,
    np,
    plot,
):
    # Lock color scale across model/dirty/calibrated so small differences are visible.
    image_min = float(
        np.min([model_image.min(), dirty_image.min(), corrected_image.min()])
    )
    image_max = float(
        np.max([model_image.max(), dirty_image.max(), corrected_image.max()])
    )

    # Use a robust symmetric range to emphasize low-level residual structure.
    dirty_residual_sigma = float(np.std(dirty_residual_image))
    calibrated_residual_sigma = float(np.std(calibrated_residual_image))
    residual_clip = 5.0 * max(dirty_residual_sigma, calibrated_residual_sigma)
    if residual_clip <= 0.0:
        residual_clip = 1.0

    mo.vstack(
        [
            mo.hstack(
                [
                    plot.plot_image(
                        model_image,
                        title="Model",
                        fov_deg=fov_slider.value,
                        zmin=image_min,
                        zmax=image_max,
                    ),
                    plot.plot_image(
                        dirty_image,
                        title="Dirty",
                        fov_deg=fov_slider.value,
                        zmin=image_min,
                        zmax=image_max,
                    ),
                    plot.plot_image(
                        corrected_image,
                        title="Calibrated",
                        fov_deg=fov_slider.value,
                        zmin=image_min,
                        zmax=image_max,
                    ),
                ],
                wrap=True,
                gap="0.1rem",
                align="start",
                widths=[1, 1, 1],
            ),
            mo.hstack(
                [
                    plot.plot_image(
                        dirty_residual_image,
                        title="Dirty - Model",
                        fov_deg=fov_slider.value,
                        zmin=-residual_clip,
                        zmax=residual_clip,
                        color_continuous_scale="RdBu_r",
                    ),
                    plot.plot_image(
                        calibrated_residual_image,
                        title="Calibrated - Model",
                        fov_deg=fov_slider.value,
                        zmin=-residual_clip,
                        zmax=residual_clip,
                        color_continuous_scale="RdBu_r",
                    ),
                ],
                wrap=True,
                gap="0.1rem",
                align="start",
                widths=[1, 1],
            ),
            mo.ui.plotly(
                plot.plot_gains(gains, station_index=gain_station_dropdown.value)
            ),
            gain_station_dropdown,
        ]
    )
    return


@app.cell
def _(mo):
    experiment_name = mo.ui.text(placeholder="your-experiment-name")
    return (experiment_name,)


@app.cell
def _(experiment_name):
    experiment_name  # pyright: ignore[reportUnusedExpression]
    return


@app.cell
def _(
    ExperimentConfig,
    corruptions_config,
    experiment_name,
    observation_config,
    sky_model_config,
    solver_config,
    telescope_config,
):
    experiment_config = ExperimentConfig(
        name=experiment_name.value if experiment_name.value else "experiment",
        skymodel=sky_model_config,
        telescope=telescope_config,
        corruptions=corruptions_config,
        observation=observation_config,
        solver=solver_config,
    )
    return (experiment_config,)


@app.cell
def _(experiment_config):
    experiment_config  # pyright: ignore[reportUnusedExpression]
    return


@app.cell
def _(mo):
    save_button = mo.ui.run_button(label="Save Experiment")
    save_button  # pyright: ignore[reportUnusedExpression]
    return (save_button,)


@app.cell
def _(experiment_config, save, save_button):
    if save_button.value:
        save(experiment_config)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## How to conduct an experiment

    1. **Configure an observation:** Move the sliders to select parameter values for your experiment. The sky model and array configuration are visualised below the sliders.
    2. **Inspect the results:** Compare the dirty image (pre-calibration) with the calibrated image and the sky model. Check the gains vary smoothly over time and frequency.
    3. **Experiment with your configuration**: Tweak the parameter values to see how they affect the images and gains.
    4. **Save a configuration**: Give your experiment a name and click the button to save the configuration. This can be re-loaded to reproduce your plots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## How results are generated

    1. **Simulate data**: an array layout, a sky model and an observation using your configuration.
    2. **Predict model visibilities**: model visibilities are generated from the simulated sky model. This is what the telescope would observe under perfect conditions.
    3. **Corrupt model visibilities**: time-dependent phase-only gains are added per station to represent what visibilities are actually observed given imperfect conditions (delays).
    4. **Calibrate observed visibilities**: a solver calculates the phase-only gains (solutions) that, when applied to observed visibilities, reproduce the model visibilities. These are then applied to observed visibilities to generate corrected visibilities.
    5. **Image**: an FFT is applied to gridded observed and corrected visibilities to generate images of the sky before and after calibration.
    """)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
