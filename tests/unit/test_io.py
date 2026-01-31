"""Tests for save and load functions."""

import pytest
from starbox.io.save import save
from pathlib import Path


@pytest.mark.parametrize("config_dir", [Path("config"), "config"])
def test_save_experiment_config(tmp_path, config_dir, experiment_config):
    """Test saving an experiment configuration to disk."""
    # Change working directory to temporary path
    import os

    os.chdir(tmp_path)

    # Save the experiment configuration
    save(experiment_config, config_dir=config_dir)

    # Check that the file was created
    expected_filename = f"{experiment_config.name.replace(' ', '_')}_config.json"
    expected_filepath = Path(config_dir) / expected_filename
    saved_file = tmp_path / expected_filepath
    assert saved_file.exists()

    # Check the contents of the file
    with open(saved_file, "r") as f:
        content = f.read()
        assert '"name": "Test Experiment"' in content
        assert '"num_stations":' in content  # Example field from telescope config
        assert '"num_sources":' in content  # Example field from skymodel config
