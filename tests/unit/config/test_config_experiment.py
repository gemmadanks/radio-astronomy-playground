""" "Tests for experiment configuration."""


def test_experiment_config_fields(
    experiment_config,
    telescope_config,
    skymodel_config,
    observation_config,
    corruptions_config,
    solver_config,
):
    """Test that ExperimentConfig initializes with correct fields."""

    assert experiment_config.name == "Test Experiment"
    assert experiment_config.telescope == telescope_config
    assert experiment_config.skymodel == skymodel_config
    assert experiment_config.observation == observation_config
    assert experiment_config.corruptions == corruptions_config
    assert experiment_config.solver == solver_config
