# Beam Model
A beam model describes the voltage response of a station as a function of direction, time and frequency. This response is due to the physical properties of the station. The beam model is used to account for beam effects when predicting visibilities.

A beam model may optionally include pointing errors, which represent beam misplacement due to mechanical or electronic pointing offsets

## Role
The beam model is evaluated during prediction to weight sky components as a function of direction, time, and frequency in order to simulate realistic observed visibilities. These simulations can be used to experiment with different effects and for testing calibration workflows with increasingly difficult tasks.

## Invariants
- Beam models are evaluated and applied to model components during predict
- A beam model is user-configurable to facilitate experimentation and learning

## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Telescope](telescope.md)
- [Predict](predict.md)
- [Corruptions](corruptions.md)
