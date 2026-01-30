"""Functions for saving experiment data to disk."""

from starbox.config.experiment import ExperimentConfig
from logging import getLogger

logger = getLogger(__name__)


def save(experiment_config: ExperimentConfig) -> None:
    """Save the experiment configuration to disk."""
    filename = f"{experiment_config.name.replace(' ', '_')}_config.json"
    with open(filename, "w") as f:
        f.write(experiment_config.model_dump_json(indent=4))
    logger.info(f"Experiment configuration saved to {filename}")
