# ADR-003: Use Marimo for exploration and Panel for scalable dashboards
| | |
| ---| ---|
| **Status** | 🟢 Accepted |
| **Created**  | 2026-01-06 |
| **Last Updated**  | 2026-02-06 |
| **Deciders** | Gemma Danks |
| **Tags** | ui |

---

## Context

Radio astronomy playground must eventually support visualisation of larger datasets required for deeper understanding of radio astronomy concepts. The choice of user interface directly affects iteration speed, transparency of intermediate results, and the ability to reason about calibration behaviour across scales.


## Problem Statement

What user interface technologies best support exploratory, reproducible self-calibration experiments while scaling to realistic radio astronomy data volumes?

## Non-goals

Radio astronomy playground will **not**:
- Provide a fully polished, multi-user web application.
- Evolve into a production-grade calibration or imaging pipeline.
- Support real-time streaming visualisation

## Decision Drivers

- Support rapid experimentation and iteration
- Support interactive visualization of large datasets (10⁶–10⁹ points) via server-side aggregation.
- Low upfront and ongoing development effort
- Integrate with scientific Python workflows
- Allow refactoring and evolution as domain understanding improves
- Preserve provenance and reproducibility of experiments

## Options Considered

|  Option  | Description | Rapid iteration | Large-scale visuals | Low effort | Python-based | Easy to refactor | Provenance | Overall score | Notes |
|----------------|-------------|-------------|-----------------|-------------| ----- | ------|------|------|------|
| **Weight**     | - | 1 | 1 | 1 | 1 | 1 | 1 | 1 | - | - |
| **Panel**      | Notebook or app   | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | 17 | Native integration with HoloViews and Datashader enables scalable interactive visualisations. Integrates well with xarray and Dask for distributed processing. |
| **Marimo**     | Reactive notebook | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | 16 | Reactive, reproducible, self-documenting. Limited to smaller datasets. |
| **Jupyter**    | Notebook          | ⚠️ | ❌ | ✅ | ✅ | ⚠️ | ✅ | 14 | Excellent for exploration and self-documenting. Limited reactive interaction. Small datasets only. |
| **Dash**       | Web app           | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ | ⚠️ | 12 | Powerful app framework. High boilerplate and slower iteration for exploratory work. |
| **Streamlit**  | Web app           | ✅ | ❌ | ⚠️ | ✅ | ❌ | ⚠️ | 12 | Very easy to prototype, but poor refactorability and slower for iterating. Limited to smaller datasets. |

✅ = 3 (good), ⚠️ = 2 (acceptable), ❌ = 1 (poor)

Overall score is a qualitative comparison aid and does not imply a single primary choice.

## Decision Outcome

Marimo will be used for prototyping and initial exploratory experiments focused on understanding radio interferometry and self-calibration through small-scale in-memory datasets. It will not be used for large-scale visualisations.

For scalable visualization of large datasets and reusable dashboards, Panel will be used in combination with the Holoviz ecosystem (HoloViews and Datashader).

## Consequences

### Good because...

- Marimo enables fast, reactive experimentation during early development and learning, which are self-documenting and reproducible.
- Panel enables interactive, large-scale visualization without requiring full recomputation of workflows when parameters change and can be used for creating standalone apps for fast feedback and exploration.
- Panel integrates well with xarray and Dask, allowing workflows to scale and run on multi-node compute clusters

### Bad because...

- Two UI technologies must be supported over time
- Some exploratory visualizations may need to be reimplemented for Panel dashboards
- Initial experiments are restricted to small-scale in-memory datasets

### Unknowns / Risks

- Additional complexity of implementing Panel dashboard apps
- Performance and usability of Panel dashboards for very large datasets
- Future ecosystem changes in Marimo or Holoviz libraries
- Interactive experimentation may encourage overfitting or parameter tuning based on visual appeal rather than scientific validity.

## Confirmation

- Core domain logic is UI-agnostic
- CI checks ensure core modules do not import UI libraries (Panel, Marimo, Holoviews).
- Exploratory workflows use Marimo notebooks/scripts
- Code will be designed with Dask and xarray in mind for future scalability
- Large-scale visualizations are implemented using HoloViews + Datashader
- Panel dashboards reuse the same plotting and analysis functions

## Links

| Type | Links |
| -----| ------|
| **ADRs**   | |
| **Issues** | |
| **PRs**    | |
