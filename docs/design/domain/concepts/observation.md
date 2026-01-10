# Observation
An observation describes how a telescope measures radio emissions in the sky.

## Representations

- A single phase centre is given as RA and Dec in radians
- Times are given as central, evenly spaced, integration times in MJD
- Frequencies are given as central frequencies of each channel
- Each channel has the same channel bandwidth given in Hz

## Role
- Used together with the geometry data from the telescope to compute baseline coordinates (UVW) as the Earth rotates
- Specifies times and frequencies for predicting ideal visibilities from a sky model
- Determines the minimum frequency and time intervals for downstream averaging and calibration solution intervals

## Invariants
- Observation parameters are independent of telescope geometry
- A single observation has a single phase centre
- Times are increasing and spaced by the same integration time
- Pointing errors are modeled in the measurement model, not as part of an observation

## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Telescope](telescope.md)
- [Predict](predict.md)
