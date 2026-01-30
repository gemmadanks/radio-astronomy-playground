import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from starbox import Imager
    from starbox.config import (
        SkyModelConfig,
        ObservationConfig,
        TelescopeConfig,
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
    from starbox.predict.predict import predict_visibilities
    from starbox.io.save import save

    return (
        CorruptionsConfig,
        ExperimentConfig,
        Imager,
        ObservationConfig,
        SkyModelConfig,
        SolverConfig,
        TelescopeConfig,
        build_corruptions,
        build_observation,
        build_skymodel,
        build_solver,
        build_telescope,
        mo,
        plot,
        predict_visibilities,
        save,
    )


@app.cell
def _():
    seed = 42
    return (seed,)


@app.cell
def _(mo):
    mo.md(r"""
    /// attention | Warning!

    This is a prototype that uses mock functions and data.
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
        initial_path="notebooks/config",
        filetypes=["yaml"],
        restrict_navigation=False,
    )
    file_browser
    return (file_browser,)


@app.cell
def _(mo):
    # Sky model
    num_sources_slider = mo.ui.slider(1, 10, label="Number of point sources: ")
    max_flux_slider = mo.ui.slider(1, 10, label="Maximum source brightness (Jy): ")
    fov_slider = mo.ui.slider(1, 10, label="Field of view (degrees): ")

    # Telescope
    num_stations_slider = mo.ui.slider(2, 100, label="Number of stations: ")
    telescope_diameter_slider = mo.ui.slider(
        1, 100, label="Maximum diameter of telescope (km): "
    )

    # Observation
    start_time_slider = mo.ui.slider(1, 100, label="Start time (MJD): ")
    observation_length_slider = mo.ui.slider(1, 100, label="Observation length: ")
    num_timesteps_slider = mo.ui.slider(1, 600, label="Number of timesteps: ")
    start_freq_slider = mo.ui.slider(
        1, 100, label="Mid-point frequency of first channel (Hz): "
    )
    num_channels_slider = mo.ui.slider(1, 100, label="Number of channels: ")
    bandwidth_slider = mo.ui.slider(1, 100, label="Total frequency bandwidth (Hz): ")

    # Corruptions
    phase_rms_slider = mo.ui.slider(
        0, 30, label="Per-station phase gain RMS (degrees): "
    )
    noise_rms_slider = mo.ui.slider(1, 100, label="Noise RMS: ")

    # Calibration
    solint_slider = mo.ui.slider(1, 600, label="Solution interval (s): ")
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
        phase_rms_slider,
        solint_slider,
        start_freq_slider,
        start_time_slider,
        telescope_diameter_slider,
    )


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
        phase_centre_deg=(0, 0),
        seed=seed,
    )
    sky_model = build_skymodel(sky_model_config)
    sky_model_fig = mo.ui.plotly(plot.plot_sky_model(sky_model))
    return sky_model, sky_model_config, sky_model_fig


@app.cell
def _(
    TelescopeConfig,
    build_telescope,
    mo,
    num_stations_slider,
    plot,
    seed,
    telescope_diameter_slider,
):
    telescope_config = TelescopeConfig(
        num_stations=num_stations_slider.value,
        diameter=telescope_diameter_slider.value,
        seed=seed,
    )
    telescope = build_telescope(telescope_config)
    telescope_fig = mo.ui.plotly(plot.plot_array_configuration(telescope))
    return telescope, telescope_config, telescope_fig


@app.cell
def _(
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
                [sky_model_fig, num_sources_slider, max_flux_slider], justify="start"
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
    start_freq_slider,
    start_time_slider,
):
    mo.vstack(
        [
            mo.hstack(
                [start_time_slider, observation_length_slider, num_timesteps_slider],
                justify="start",
            ),
            mo.hstack(
                [start_freq_slider, num_channels_slider, bandwidth_slider],
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
    start_freq_slider,
    start_time_slider,
):
    observation_config = ObservationConfig(
        start_time=start_time_slider.value,
        observation_length=observation_length_slider.value,
        num_timesteps=num_timesteps_slider.value,
        start_frequency=start_freq_slider.value,
        num_channels=num_channels_slider.value,
        total_bandwidth=bandwidth_slider.value,
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
def _(mo, noise_rms_slider, phase_rms_slider):
    mo.hstack([noise_rms_slider, phase_rms_slider], justify="start")
    return


@app.cell
def _(
    CorruptionsConfig,
    build_corruptions,
    noise_rms_slider,
    phase_rms_slider,
    seed,
):
    corruptions_config = CorruptionsConfig(
        rms_noise=noise_rms_slider.value,
        rms_phase_gain=phase_rms_slider.value,
        seed=seed,
    )
    corruptions = build_corruptions(corruptions_config)
    return corruptions, corruptions_config


@app.cell
def _(SolverConfig, build_solver, solint_slider):
    solver_config = SolverConfig(solint=solint_slider.value)
    solver = build_solver(solver_config)
    return solver, solver_config


@app.cell
def _(Imager):
    imager = Imager()
    return (imager,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Results
    """)
    return


@app.cell
def _(
    corruptions,
    imager,
    num_stations_slider,
    observation,
    predict_visibilities,
    sky_model,
    solver,
    telescope,
):
    model_visibilities = predict_visibilities(telescope, sky_model, observation)
    observed_visibilities = corruptions.apply(model_visibilities)
    gains = solver.solve(
        observed_visibilities, model_visibilities, num_stations_slider.value
    )
    corrected_visibilities = gains.apply(observed_visibilities)

    dirty_image = imager.image(observed_visibilities)
    corrected_image = imager.image(corrected_visibilities)
    return corrected_image, dirty_image, gains


@app.cell
def _(corrected_image, dirty_image, gains, mo, plot):
    mo.vstack(
        [
            mo.hstack(
                [
                    plot.plot_image(dirty_image, title="Dirty"),
                    plot.plot_image(corrected_image, title="Calibrated"),
                ]
            ),
            plot.plot_gains(gains),
        ]
    )
    return


@app.cell
def _(mo):
    experiment_name = mo.ui.text(placeholder="your-experiment-name")
    return (experiment_name,)


@app.cell
def _(experiment_name):
    experiment_name
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
        name=experiment_name.value,
        skymodel=sky_model_config,
        telescope=telescope_config,
        corruptions=corruptions_config,
        observation=observation_config,
        solver=solver_config,
    )
    return (experiment_config,)


@app.cell
def _(experiment_config):
    experiment_config
    return


@app.cell
def _(mo):
    save_button = mo.ui.run_button(label="Save Experiment")
    save_button
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
