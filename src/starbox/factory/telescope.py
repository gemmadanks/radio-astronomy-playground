"""Functions to build telescopes."""

from starbox.simulate.telescope import Telescope
from starbox.config.telescope import TelescopeConfig


def build_telescope(cfg: TelescopeConfig, name="Telescope") -> Telescope:
    """Build a Telescope from a TelescopeConfig.

    Args:
        cfg (TelescopeConfig): Configuration for the telescope.

    Returns:
        Telescope: The constructed telescope.
    """
    return Telescope(cfg, name=name)
