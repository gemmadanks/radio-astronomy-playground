"""Functions to build sky models."""

from starbox.simulate.skymodel import SkyModel, SkyModelSpec
from starbox.config.skymodel import SkyModelConfig


def build_skymodel(cfg: SkyModelConfig) -> SkyModel:
    """Build a SkyModel from a SkyModelConfig.

    Args:
        cfg (SkyModelConfig): Configuration for the sky model.

    Returns:
        SkyModel: The constructed sky model.
    """
    spec = SkyModelSpec(**cfg.model_dump())
    return SkyModel.from_spec(spec)
