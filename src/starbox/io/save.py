"""Functions for saving experiment data to disk."""

from starbox.config.experiment import ExperimentConfig
from logging import getLogger
from pathlib import Path

logger = getLogger(__name__)


def save(
    experiment_config: ExperimentConfig, config_dir: Path | str = Path("config")
) -> None:
    """Save the experiment configuration to disk.

    Args:
        experiment_config: The ExperimentConfig instance to save.
        config_dir: The directory to save the configuration file in.
    """
    config_dir = Path(config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    filename = config_dir / f"{experiment_config.name.replace(' ', '_')}_config.json"
    with open(filename, "w") as f:
        f.write(experiment_config.model_dump_json(indent=4))
    logger.info(f"Experiment configuration saved to {filename}")
