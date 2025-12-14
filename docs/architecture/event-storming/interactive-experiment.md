
# Interactive Experiment

## Scenario

A user interactively modifies station layout, observation parameters, and instrument models and immediately sees how the final image products change. The primary goal is **conceptual exploration and algorithm intuition**, not production-scale processing.

---

## Scope

* Simulation-based
* Small datasets
* Fast feedback (seconds, not minutes)
* Panel app with sliders, toggles, and dropdown widgets

Out of scope:

* Calibration (including self-calibration)
* Large datasets

---

## Layered Event Storming View

This workflow has **three layers**:

1. Commands (user intent)
2. Domain events (facts that happened)
3. Views (what is displayed)

---

## 1. Commands (User Intent)

These map to notebook widgets.

### Array configuration

* Select array layout (example or custom)
* Add station
* Remove station
* Modify station positions

### Observation setup

* Set integration time
* Set total observation duration
* Set frequency setup
* Set phase center

### Sky & instrument

* Select sky model
* Select primary beam model
* Enable / disable corruption models
* Set noise level
* Set gain / phase error parameters

### Imaging

* Select weighting scheme (natural / uniform / robust)
* Set image size and cell size
* Set deconvolution parameters

---

## 2. Domain Events (What Happens)

### Configuration

* Site location specified
* Array configuration defined
* Observation setup defined
* Sky model selected
* Instrument model defined
* Primary beam model selected
* Visibility averaging policy defined

### Simulation

* UVW sampling computed
* Sky model visibilities predicted
* Instrument corruptions applied
* Visibilities averaged

### Imaging

* Visibilities gridded
* Dirty image generated
* PSF generated
* Deconvolution performed
* Model image generated
* Residual image generated

### Iteration

* Parameters updated
* Affected intermediate products invalidated
* Required products recomputed

---

## 3. Views (Projections)

These are derived, read-only views of the domain state.

* UV coverage displayed
* Dirty image displayed
* PSF displayed
* Model image displayed
* Residual image displayed
* Restored image displayed

Views do **not** trigger domain changes by themselves.

---

## Core Aggregates

### Experiment

Represents a single interactive experiment.

Responsibilities:

* Owns current configuration
* Tracks derived products and caches
* Decides what must be recomputed when parameters change

---

### Telescope

Includes site location, station positions, and derived baselines.

Invariants:

* Station identifiers are unique
* Positions share a common coordinate frame
* Baselines are derived solely from station positions

---

### Observation

Includes time and frequency configuration and pointing.

Invariants:

* Integration time divides observation duration
* Frequency grid is consistent with channelization
* Phase center is well-defined

---

### SkyModel

Defines the true sky used for simulation.

Invariants:

* Flux units are consistent
* Spectral models are defined over the observation band

---

### InstrumentModel

Defines corruptions and beam effects.

Invariants:

* Beam model matches frequency range
* Corruption parameterization is internally consistent

---

### VisibilitySet

Contains predicted, corrupted, and averaged visibilities.

Invariants:

* Array shapes are consistent across visibilities, flags, and weights
* UVW coordinates align with time/baseline axes
* Units are fixed (e.g. meters, Hz)

---

### DataProducts

Contains image-plane products.

Invariants:

* Dirty image, PSF, model, and residual share a common grid
* Residual = dirty − (model ⊗ PSF)

---

## Dependency & Recompute Map

This dependency graph determines cache invalidation when parameters change.

```mermaid
flowchart LR
  A[Telescope] --> U[UVW]
  O[Observation] --> U
  S[SkyModel] --> Vp[Predicted visibilities]
  U --> Vp
  I[Corruptions] --> Vc[Corrupted visibilities]
  Vp --> Vc
  O --> Va[Averaged visibilities]
  Vc --> Va
  Va --> G[Gridded visibilities]
  O --> G
  G --> D[Dirty image]
  G --> P[PSF]
  D --> C[Deconvolution]
  P --> C
  C --> M[Model image]
  C --> R[Residual image]
  ```

Examples:

* Changing **integration time** invalidates averaged visibilities and downstream products.
* Changing **array layout** invalidates UVW sampling and everything downstream.
* Changing **beam model** invalidates corrupted visibilities and downstream products.
* Changing **imaging weighting** invalidates gridded visibilities and image products only.

---

## Notes for Implementation

* Widgets issue **commands**; they do not directly run algorithms.
* The Experiment aggregate coordinates recomputation.
* Algorithms remain stateless and reusable.
* The domain model is independent of notebooks and plotting.

This document serves as the architectural anchor for interactive experiments.
