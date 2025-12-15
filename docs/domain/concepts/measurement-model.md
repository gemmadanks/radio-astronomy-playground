# Measurement Model (Corruptions and Beams)
A measurement model represents how the true signal from the sky is transformed to generate the observed signal. It accounts for the difference between ideal visibilities (i.e. visibilities predicted from a perfect sky model) and observed visibilities that are effects not explained by the sky model and array geometry. This includes effects originating from the telescope hardware (instrumental effects) as well as the propagation medium between the sources and the telescope (e.g. the atmosphere).

## Measurement effects
Measurement effects are optionally applied in order of decreasing proximity to the sky model *after* predicting model visibilities.

### Beam model
The beam model describes the voltage response of a station as a function of direction, time and frequency. This response is due to the physical properties of the station. The beam model is used to apply beam effects prior to corruptions.

### Corruptions
Corruptions describe a set of transformations in visibility space in order to simulate different measurement effects.

1. **Pointing errors**: effective beam misplacement due to mechanical or electronic pointing offsets
2. **Phase screen**: time- and baseline-dependent phase errors due to variations in the ionosphere, usually direction-dependent and can blur images if not corrected
3. **Delays / clocks**: linear phase vs. frequency
4. **Bandpass**: gains due to frequency-dependent effects on different channels
5. **Complex gains**: per station time and frequency dependent variability in phase and amplitude, assumed to be constant over a calibration solution interval
6. **Thermal noise**: additive random noise from receiver and sky, sets the sensitivity limit of an observation.

Missing and flagged data can also be simulated.

## Role
Corruptions are applied to predicted model visibilities in order to simulate realistic observed visibilities. These simulations can be used to experiment with different effects and for testing calibration workflows with increasingly difficult tasks.

## Invariants
- Corruptions and beam model effects are applied to visibilities after predict
- Measurement effects are applied in order of decreasing proximity to the sky model: beam -> pointing -> phase screen -> delays -> bandpass -> complex gains -> noise.
- Random processes (e.g. noise) are reproducible for a given set of parameters and random seed
- Corruptions transform visibilities to produce modified visibilities
- Beam models do not directly modify visibilities
- A measurement model is user-configurable to facilitate experimentation and learning

## Related concepts
- [Averaging](averaging.md)
- [Calibration](calibration.md)
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Self-calibration](self-calibration.md)
- [Telescope](telescope.md)
- [Predict](predict.md)
