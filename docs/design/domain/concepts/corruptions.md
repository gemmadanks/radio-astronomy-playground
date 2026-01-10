# Corruptions
Corruptions represent how the true signal from the sky is transformed into the observed signal. They account for the difference between ideal visibilities (i.e. visibilities predicted from a perfect sky model) and observed visibilities that are effects not explained by the sky model, beam model and array geometry. This includes effects originating from the telescope hardware (instrumental effects) as well as the propagation medium between the sources and the telescope (e.g. the atmosphere).

Corruptions describe a set of transformations in visibility space in order to simulate different measurement effects. Corruptions are optionally applied in order of decreasing proximity to the sky model *after* predicting model visibilities.

1. **Phase screen**: time- and baseline-dependent phase errors due to variations in the ionosphere, usually direction-dependent and can blur images if not corrected
2. **Delays / clocks**: linear phase vs. frequency
3. **Bandpass**: gains due to frequency-dependent effects on different channels
4. **Complex gains**: per station time and frequency dependent variability in phase and amplitude, assumed to be constant over a calibration solution interval
5. **Thermal noise**: additive random noise from receiver and sky, sets the sensitivity limit of an observation.

Missing and flagged data can also be simulated.

## Role
Corruptions are applied to predicted model visibilities in order to simulate realistic observed visibilities. These simulations can be used to experiment with different effects and for testing calibration workflows with increasingly difficult tasks.

## Invariants
- Corruptions are applied to visibilities after predict in order of decreasing proximity to the sky model: phase screen -> delays -> bandpass -> complex gains -> noise.
- Additive effects (noise) are always applied last.
- Random processes (e.g. noise) are reproducible for a given set of parameters and random seed
- Applying corruptions transforms visibilities to produce modified visibilities
- Corruptions are user-configurable to facilitate experimentation and learning

## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Telescope](telescope.md)
- [Predict](predict.md)
- [Beam Model](beam-model.md)
