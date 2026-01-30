"""Tests for save and load functions."""

from starbox.io.save import save


def test_save_experiment_config(tmp_path, experiment_config):
    """Test saving an experiment configuration to disk."""
    # Change working directory to temporary path
    import os

    os.chdir(tmp_path)

    # Save the experiment configuration
    save(experiment_config)

    # Check that the file was created
    expected_filename = f"{experiment_config.name.replace(' ', '_')}_config.json"
    saved_file = tmp_path / expected_filename
    assert saved_file.exists()

    # Check the contents of the file
    with open(saved_file, "r") as f:
        content = f.read()
        assert '"name": "Test Experiment"' in content
        assert '"num_stations":' in content  # Example field from telescope config
        assert '"num_sources":' in content  # Example field from skymodel config
