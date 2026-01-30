"""Functions to build telescopes."""

from starbox.simulate.telescope import Telescope, TelescopeSpec
from starbox.config.telescope import TelescopeConfig


def build_telescope(cfg: TelescopeConfig) -> Telescope:
    """Build a Telescope from a TelescopeConfig.

    Args:
        cfg (TelescopeConfig): Configuration for the telescope.

    Returns:
        Telescope: The constructed telescope.
    """
    spec = TelescopeSpec(**cfg.model_dump())
    return Telescope.from_spec(spec)
