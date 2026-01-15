# S1: Self-calibration loop + diagnostics (MVP)

This page documents the functional requirements for a minimal viable product (MVP) for Radio Astronomy Playground, corresponding to deliverable slice 1 shown in the [impact map](../vision/impact-map.md). They are formulated as user stories with behaviour-driven-design (BDD) scenarios that form the basis for issues tracked in GitHub and BDD tests respectively.

## Assumptions

- Calibration is performed at the **station** level (one complex gain per station) and is phase-only
- Visibilities are scalar (Stokes I) and stored as complex64/complex128.
- Visibilities have shape (n_timesteps, n_baselines, n_channels).

## STAR-001: Reproducible randomly generated simulations

### User story
>**As a** Radio Astronomy Learner
>
>**I want** to simulate data (visibilities) and models (sky model, telescope, observation, corruptions) with a seed
>
>**so that** I can reproduce the same simulation and compare results of different experiments.

### BDD scenarios
- **Given** a simulation configuration with a fixed seed

  **When** I configure the simulation twice

  **Then** the sky model, station layout, and observation sampling are identical

- **Given** two simulation configurations with different seeds

  **When** I configure the simulation twice

  **Then** at least one of sources or station positions differs

- **Given** a simulation configuration without a seed

  **When** I configure the simulation twice

  **Then** the results differ

## STAR-002: Predicted visibilities
### User story
>**As a** Radio Astronomy Learner
>
>**I want** to predict visibilities from a sky model
>
>**so that** I can understand what an interferometer would observe under perfect conditions and I have a reference dataset for calibration

### BDD scenarios
- **Given** a sky model with a single point source at the phase centre

  **When** I predict visibilities

  **Then** phase is approximately constant across baselines within tolerance

- **Given** a sky model with a single point source offset from the phase centre

  **When** I predict visibilities

  **Then** visibility phase varies with baseline consistent with geometric delay

## STAR-003: Corruptions and noise applied to visibilities

### User story
>**As a** Radio Astronomy Learner
>
>**I want** to apply known phase-only corruptions and noise to visibilities
>
>**so that** I can create controlled "observed" visibilities from model visibilities and understand how instrumental effects modify the data

### BDD scenarios
- **Given** identity gains and zero noise

  **When** I corrupt model visibilities

  **Then** observed visibilities are identical to model visibilities (within tolerance)

- **Given** phase gains and zero noise

  **When** I corrupt model visibilities

  **Then** baseline phase differences in corrupted visibilities reflect the applied gains

- **Given** non-zero noise

  **When** I corrupt model visibilities

  **Then** observed visibilities differ from model visibilities with the expected RMS level

## STAR-004: Solve for phase-only gains

### User story
>**As a** Radio Astronomy Learner
>
>**I want** to solve for phase-only gains with specified time and frequency solution intervals in corrupted visibilities vs. model visibilities
>
>**so that** I can understand how calibration corrects for instrumental effects

### BDD scenarios
- **Given** noise-free model visibilities with known phase-only gains applied

  **When** I solve for phase-only gains with correct solution intervals

  **Then** solved gains match the applied gains

- **Given** noisy model visibilities with known phase-only gains applied

  **When** I solve for phase-only gains with correct solution intervals

  **Then** there are no NaN or Inf values in the solutions

## STAR-005: Apply phase-only calibration solutions

### User story
>**As a** Radio Astronomy Learner
>
>**I want** to apply phase-only calibration solutions to corrupted visibilities to generate corrected visibilities
>
>**so that** I can understand how calibration corrects for instrumental effects

### BDD scenarios
- **Given** noise-free model visibilities with known phase-only gains applied and calibration solutions

  **When** I apply the calibration solutions

  **Then** corrected visibilities match model visibilities

- **Given** noisy model visibilities with known phase-only gains applied and calibration solutions

  **When** I apply the calibration solutions

  **Then** there are no NaN or Inf values and corrected visibilities have the expected RMS level

## STAR-006: Image visibilities

### User story
>**As a** Radio Astronomy Learner
>
>**I want** to generate images of model, observed and corrected visibilities
>
>**so that** I can inspect the impact of calibration and instrumental effects

### BDD scenarios
- **Given** visibilities of a point source at the phase centre

  **When** I generate an image

  **Then** the brightest pixels is in the centre of the image

- **Given** predicted visibilities from a sky model of 3-5 bright point sources

  **When** I generate an image

  **Then** the positions of the brightest pixels align with the positions of the point sources in the sky model image

- **Given** corrupted visibilities before and after calibration solutions are applied

  **When** I generate images for each visibility set

  **Then** the image of visibilities after calibration is closer to the image of the sky model

## STAR-007: Diagnostic plots and statistics

### User story
>**As a** Radio Astronomy Learner
>
>**I want** summary statistics and plots of diagnostic metrics after every self-calibration loop
>
>**so that** I can evaluate convergence, divergence, over-fitting and failures of self-calibration

### BDD scenarios
- **Given** a completed self-calibration loop

  **When** I request diagnostics

  **Then** I get: images and statistics on residuals before and after calibration and plots of phase gain vs. time for selected stations.

- **Given** a failed self-calibration loop

  **When** I request diagnostics

  **Then** the diagnostics have at least one warning indicating a failure.

## STAR-008: Save and load experiments

### User story
>**As a** Radio Astronomy Learner
>
>**I want** to save and reload an experiment
>
>**so that** I can re-inspect results and compare to other experiments

### BDD scenarios
- **Given** a completed self-calibration experiment

  **When** I save the plots, configuration and final calibration loop datasets and reload them later

  **Then** I get the same plots, configuration and data sets and can regenerate the same diagnostic outputs

- **Given** two completed self-calibration experiments

  **When** I reload both

  **Then** I can compare results side-by-side

## Acceptance criteria for MVP
1. Results and diagnostics for at least one for each of the following self-calibration runs are saved and can be reloaded:
    - Converged: images stop improving and solutions are stable over time
    - diverged: images start to get worse and solutions become less stable over iterations
    - failed: valid solutions cannot be found
    - overfitted: images improve but solutions become less stable over time
2. Each run can be reproduced from a notebook

## Out of scope (MVP)

- Beam/DDE effects
- w-term correction
- CLEAN/deconvolution
- Full-Jones calibration
- Distributed execution / large datasets
- Dashboard UI
