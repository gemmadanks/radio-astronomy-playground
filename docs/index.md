# Welcome to Radio Astronomy Playground

Radio Astronomy Playground is a learning and experimentation environment for
understanding radio interferometry, calibration, imaging, and self-calibration.
It is motivated by the difficulty of developing intuition for these workflows,
which often involve many interacting parameters and iterative decisions.
It includes:

- ✨ **Starbox** — a Python package that serves as the core library for all
  experiments and visualisations. It provides simple implementations of key
  radio astronomy concepts (e.g. sky models, interferometers, visibility
  prediction, calibration loops).
- 📚 **Interactive experiments** — notebooks and dashboards that allow you to
   explore how calibration and imaging behaviour changes as parameters,
   assumptions, and models vary.

This project is designed for **learning**, not as a replacement for
production pipelines.

---

## For learners and users

Explore the user documentation if you want to run experiments and build
intuition for radio astronomy concepts through hands-on exploration:

- [**Tutorials**](tutorials/index.md) — guided, step-by-step introductions
- [**How-to guides**](how-to/index.md) — workflows for specific tasks
- [**Explanations**](explanation/index.md) — conceptual background information
- [**Reference**](reference/index.md) — API documentation

---

## For contributors and collaborators

Explore the design documentation if you are interested in contributing,
extending, or understanding the design of the project:

- [**Design**](design/index.md) – architectural decisions, domain exploration,
  and prioritisation artefacts (including impact maps and ADRs).

---

## Project scope and philosophy

Radio Astronomy Playground focuses on:

- Optimising for insight rather than performance or scalability
- Interactive experiments and diagnostics over automated pipelines
- Failure modes as well as successful outcomes
- Clean, readable code and smooth user experience as enablers of learning

Many features are intentionally simplified to keep behaviour visible and
interpretable.

The project is under active development. Interfaces, experiments, and
documentation will evolve as understanding improves.
