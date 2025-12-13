# Sky model

A sky model is a representation of the positions, shapes, and brightness of radio-emitting sources on the sky, including their frequency-dependence.

Each source or component may include:
- Position in right ascension (RA) and declination (Dec) in degrees, radians or sexagesimal hours, minutes and seconds.
- Brightness (flux density) in Jansky for one or more Stokes parameters (I, Q, U, V).
- Shape (for extended sources) specified as:
    - Width along major (longest) and minor (shortest) axes at full width half maximum (FWHM) in arcseconds
    - Orientation of the major axis in degrees eastward from North
- Spectral index at a reference frequency (dimensionless), indicating whether the emission is synchrotron (negative) or thermal (positive).
- Optionally, an association with a patch, representing a cluster of sources treated together (e.g. for direction-dependent calibration).

## Representations

- An image or image cube (pixel-based model).
- A list or source catalog.

## Role
A sky model represents an estimate of the true sky. It can be an existing model extracted from a sky survey database or an output of the image cleaning or source-finding process. It is used to:

- Predict model visibilities for calibrating observed visibilities to remove corruptions.
- Iteratively improve images produced via self-calibration.

## Invariants
- A sky model is defined with respect to a specific phase centre, coordinate frame and field of view.
- Flux densities are expressed per Stokes parameter.
- A sky model is valid only over the time and frequency range for which it was derived.
- Each source belongs to at most one patch within a given sky model.

## Related concepts
- [Stokes parameters](stokes-parameters.md)
- [Calibration](calibration.md)
- [Imaging](imaging.md)
- [Predict](predict.md)
- [Self-calibration](self-calibration.md)
