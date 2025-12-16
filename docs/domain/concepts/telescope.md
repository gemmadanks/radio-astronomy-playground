# Telescope
A telescope is the term used to collectively describe one or more stations (dish or array of antennas), each of which can be "pointed" (digitally or physically) along a line of sight given by specifying a phase centre (location on the sky). When there is more than one station the telescope functions as an interferometer. Each station forms a beam on the sky. A pair of stations forms a baseline and their signals are inputs to a correlator which outputs visibilities. The layout of stations determines how signals from the sky are sampled as Earth rotates.


## Role
The geometric properties of a telescope, together with the parameters of an observation, define:
- Baselines used when predicting visibilities
- UV-coverage to evaluate how the signals from the sky are sampled
- Parameters to tweak for simulating the effects of telescope geometry on data products

## Invariants
- Station IDs are unique for a given telescope
- The centre of each station has a position relative to the telescope site and is given as East (m), North (m) and up (m) coordinates.
- The location of the centre of a telescope ("site") is given in longitude (deg), latitude (deg) and height (m).
- Beams are formed at the station level.
- Telescope geometry is fixed over a given observation
- Each antenna element belongs to a single station

## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Predict](predict.md)
- [Observation](observation.md)
