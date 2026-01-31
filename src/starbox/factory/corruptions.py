"""Functions to build corruptions."""

from starbox.config.corruptions import CorruptionsConfig
from starbox.simulate.corruptions import Corruptions


def build_corruptions(cfg: CorruptionsConfig) -> Corruptions:
    """Build a Corruptions instance from a CorruptionsConfig.

    Args:
        cfg: The CorruptionsConfig instance.
    Returns:
        A Corruptions instance.
    """
    return Corruptions(cfg)
