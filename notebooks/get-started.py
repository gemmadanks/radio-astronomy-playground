import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from starbox import Telescope, SkyModel

    return SkyModel, Telescope, mo


@app.cell
def _():
    seed = 42
    return (seed,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # ✨ Welcome to [Radio Astronomy Playground](https://open-research.gemmadanks.com/radio-astronomy-playground/)! ✨
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## How to conduct an experiment
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    Follow the steps outlined below to set up and execute an experiment.
    """)
    return


@app.cell
def _(mo):
    mo.accordion(
        items={
            "1. Configure an experiment": """Choose the number of radio sources in the sky, number of stations in your telescope and its diameter, and how many time steps and frequency channels you want to include in your observation.""",
            "2. Simulate a sky model": """Radio point sources will be randomly positioned on the sky.""",
            "3. Predict model visibilities": """Generate 'perfect' ('true') visibilities for your sky model.""",
            "4. Corrupt model visibilities": """Select and apply corruptions to simulate observed visibilities.""",
            "5. Image 'observed' visibilities": """Generate a dirty image of the sky with corruptions.""",
            "6. Calibrate 'observed' visibilities": """Select calibration parameters and solve for solutions using model visibilities.""",
            "7. Apply solutions": """Apply calibration solutions to 'observed' visibilities to get 'corrected' visibilities.""",
            "8. Image 'corrected' visibilitites": """""",
            "9. Experiment": """Adjust the parameters of your experiment and see how the final image changes""",
        }
    )
    return


@app.cell
def _(mo):
    mo.md("""
    ## 1. Configure an experiment
    """)
    return


@app.cell
def _(mo):
    # Sky model
    num_sources_slider = mo.ui.slider(1, 10, label="Number of point sources: ")
    max_flux_slider = mo.ui.slider(1, 10, label="Maximum source brightness (Jy): ")
    # Telescope
    num_stations_slider = mo.ui.slider(1, 100, label="Number of stations: ")
    telescope_diameter_slider = mo.ui.slider(
        1, 100, label="Maximum diameter of telescope (km): "
    )
    return (
        max_flux_slider,
        num_sources_slider,
        num_stations_slider,
        telescope_diameter_slider,
    )


@app.cell
def _(num_sources_slider):
    num_sources_slider
    return


@app.cell
def _(max_flux_slider):
    max_flux_slider
    return


@app.cell
def _(num_stations_slider):
    num_stations_slider
    return


@app.cell
def _(telescope_diameter_slider):
    telescope_diameter_slider
    return


@app.cell
def _(SkyModel, max_flux_slider, num_sources_slider, seed):
    sky_model = SkyModel(
        name="My Sky Model",
        num_sources=num_sources_slider.value,
        max_flux=max_flux_slider.value,
        seed=seed,
    )
    return (sky_model,)


@app.cell
def _(mo, sky_model):
    sky_model_fig = mo.ui.plotly(sky_model.plot(show=False))
    return (sky_model_fig,)


@app.cell
def _(sky_model_fig):
    sky_model_fig
    return


@app.cell
def _(Telescope, num_stations_slider, seed, telescope_diameter_slider):
    telescope = Telescope(
        name="My Telescope",
        num_antennas=num_stations_slider.value,
        diameter=telescope_diameter_slider.value,
        seed=seed,
    )
    return (telescope,)


@app.cell
def _(mo, telescope):
    telescope_fig = mo.ui.plotly(telescope.plot(show=False))
    return (telescope_fig,)


@app.cell
def _(telescope_fig):
    telescope_fig
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
