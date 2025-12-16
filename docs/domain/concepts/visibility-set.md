# Visibility Set
A VisibilitySet represents a collection of interferometric measurements produced by correlating signals from pairs of stations (baselines). Each visibility represents the spatial coherence of the sky at a specific baseline, time, polarization and frequency.

## Representations
- An array of complex values (representing amplitude and phase) indexed by baseline, time, frequency, and polarization.
- UVW baseline coordinates (m) derived from telescope and observation parameters
- Optional weights and flags per visibility.

## Role
Inputs and outputs for:
- Calibration (model visibilities are compared to observed visibilities)
- Applying corruptions or beam effects (measurement model)
- Subtraction (model visibilities from residual visibilities) during a major cycle in CLEAN-like deconvolution algorithms
- Averaging over time and/or frequency

Inputs for:
- Gridding (visibilities are mapped to a grid in a 2D uv-plane)

## Invariants
- UVW coordinates are defined relative to the observation phase centre.
- All per-visibility arrays within a VisibilitySet are aligned: the same index refers to the same baseline, time, frequency, and polarization across all fields.
- Time and frequency axes are ordered.
- Averaging produces a new effective sampling (time/frequency centres and widths).
- Transformations produce new visibility sets rather than modifying the conceptual meaning of the original.


## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Telescope](telescope.md)
- [Observation](observation.md)
