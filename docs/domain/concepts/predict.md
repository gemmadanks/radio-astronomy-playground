# Predict

Predict refers to the process of computing ideal interferometric visibilities from a sky model using a specific configuration of an interferometer and observation. It is used to "predict" what an interferometer would measure, under these conditions in the absence of corruptions (e.g. instrumental or atmospheric effects) and is usually done with high time and frequency resolution.

## Inputs
- A sky model (locations and fluxes of radio sources in the sky)
- Array geometry (station positions and derived baselines)
- Observation parameters (frequency and time intervals, phase centre)

## Outputs
- A set of complex visibilities per baseline, time, freq, polarization.

## Role
Predict is essential for several workflows that require ideal visibilities to be computed. These include:
- Synthetic visibilities for simulations and tests. These may have corruptions applied after prediction.
- Model visibilities for calibrating observed visibilities.
- Model visibilities that are subtracted from observed visibilities to generate residual visibilities during self-calibration.

## Invariants
- Predict does not introduce corruptions
- Corruptions are applied after predict
- Averaging is performed after predict
- Predict is deterministic
- Predict is defined relative to a specific phase centre and coordinate frame

## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Telescope](telescope.md)
- [Beam Model](beam-model.md)
