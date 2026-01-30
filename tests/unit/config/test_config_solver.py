"""Tests for solver configuration."""

from starbox.config.solver import SolverConfig
import pytest
from pydantic import ValidationError
from starbox.calibrate.solver import SolverSpec


def test_solver_config_from_dict():
    parameter_dict = {
        "solint": 10,
    }
    solver_config = SolverConfig(**parameter_dict)
    for key, value in parameter_dict.items():
        assert getattr(solver_config, key) == value


def test_solver_config_valid():
    cfg = SolverConfig(solint=10)
    assert cfg.solint == 10


def test_solver_config_rejects_bad_solint():
    with pytest.raises(ValidationError):
        SolverConfig(solint=0)
    with pytest.raises(ValidationError):
        SolverConfig(solint=-5)


def test_solver_config_roundtrip_json():
    cfg = SolverConfig(solint=10)
    cfg2 = SolverConfig.model_validate_json(cfg.model_dump_json())
    assert cfg2 == cfg


def test_solver_config_to_spec():
    cfg = SolverConfig(solint=10)
    spec = SolverSpec(**cfg.model_dump())
    assert spec.solint == cfg.solint
