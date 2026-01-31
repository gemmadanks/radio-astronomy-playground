# ADR-004: Use Pydantic models for configuration schemas

| | |
| ---| ---|
| **Status** | 🟢 Accepted |
| **Created** | 2026-01-31 |
| **Last Updated** | 2026-01-31 |
| **Deciders** | Gemma Danks |

---

## Context

Configuration objects are used to define parameters for:

- Simulating data, such as sky models, array configurations, observations and corruptions.
- Processing data, such as calibration solver parameters and imaging parameters.
- Setting random seeds.
- Reproducing an experiment defined by the above.

These configurations are:

- Edited interactively in notebooks and dashboards (via widgets or code cells)
- Saved and reloaded for reproducibility (in json format)
- Passed into classes to construct simulations
- Used in automated tests and CI fixtures

The project prioritises:

- Reproducibility and provenance
- Inspectability and transparency
- Scientific validity
- Modularity between UI, configuration, and core domain logic
- Low friction for experimentation

Configuration objects therefore need:

- Strong validation
- Clear schemas
- Easy serialisation/deserialisation
- Good ergonomics in notebooks
- Explicit constraints (e.g. positive counts, ranges)

Multiple approaches were considered for representing configuration:
plain dictionaries, dataclasses, and Pydantic models.

---

## Problem Statement

What representation should be used for configuration schemas (e.g. SkyModel, Telescope, Observation, Corruptions)
to balance validation, reproducibility, usability, and modularity?

---

## Options Considered

Decision drivers:

- **Validation & constraints** — ability to express and enforce parameter bounds
- **Reproducibility & serialisation** — easy save/load of configurations
- **Developer experience** — clarity in notebooks and code
- **Modularity** — clean separation between configuration and domain logic
- **Maintenance effort** — avoiding duplicated validation logic

| Option | Description | Validation | Reproducibility | Developer Experience | Modularity | Maintenance | Overall | Notes |
|--------|-------------|------------|------------------|------------|-----------|-------------|---------|------|
| **Weight** | - | 1 | 1 | 1 | 1 | 1 | - | - |
| Plain dicts | Use raw Python dictionaries | ❌ | ⚠️ | ❌ | ⚠️ | ❌ | Low | No schema, no validation, fragile |
| Dataclasses | Use Python dataclasses for configs | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | Medium | Requires manual validation and serialization |
| Pydantic models | Use Pydantic BaseModel for configs | ✅ | ✅ | ✅ | ✅ | ✅ | High | Built-in validation, typing, and serialization |

Legend: ✅ = 3 ⚠️ = 2 ❌ = 1

---

## Decision Outcome

We will use **Pydantic models** as the canonical representation for configuration schemas.

Pydantic provides:

- Declarative validation (e.g. bounds, required fields)
- Typed access to parameters
- Built-in serialisation (`model_dump`, `model_validate`)
- Clear schemas for documentation and UI generation
- Reduced duplicated validation logic compared to dataclasses and manual checks

Domain objects (e.g. `SkyModel`, `Telescope`) will accept Pydantic config objects directly rather than raw dictionaries.
`model_dump()` is only used at I/O boundaries (saving to disk, logging, transport).


---

## Consequences

### Good

- Configuration constraints are explicit and enforced at construction time
- Experiments are easily serialised and replayed
- Notebook UX is improved through typed models
- Domain code avoids duplicated validation logic
- Clear separation between configuration (Pydantic) and behaviour (domain classes)
- Supports future pipeline use cases

### Bad

- Introduces Pydantic as a core dependency
- Slight learning curve for contributors unfamiliar with Pydantic
- Domain classes depend on an external library for configuration types

### Unknowns / Risks

- Pydantic version changes may affect APIs
- Performance impact is negligible for MVP but may impact scaling later
- Tight coupling between config schemas and domain constructors

---

## Confirmation

This ADR will be enforced by:

- Domain constructors accepting Pydantic config objects directly
- Avoiding `model_dump()` inside core logic (only at I/O boundaries)
- Code reviews checking for raw dict-based configs
- Documentation examples consistently using Pydantic models
- Tests using Pydantic fixtures for canonical configurations

---

## Links

| Type | Links |
| -----| ------|
| **ADRs** | |
| **Issues** | https://github.com/gemmadanks/radio-astronomy-playground/issues/33 |
| **PRs** | https://github.com/gemmadanks/radio-astronomy-playground/pull/55 |
