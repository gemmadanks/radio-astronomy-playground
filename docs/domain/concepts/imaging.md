# Imaging
Imaging is the process of transforming interferometric measurements of the sky from Fourier space (visibilities) into image space (pixels) in order to produce a visual representation of the sky brightness distribution.

Imaging involves mapping irregularly sampled visibilities onto a regular grid in the uv-plane and forming an image via an inverse Fourier transform, which represents the sky convolved with the point-spread function (PSF) of the interferometer. Deconvolution techniques are typically used to estimate the underlying sky brightness distribution by accounting for the effects of incomplete uv-coverage.

## Deconvolution
This step in imaging iteratively builds a sky model by identifying significant structure in the dirty image, subtracting the PSF response of that structure, and repeating until the residuals are consistent with noise.

CLEAN is a class of algorithms (including Högbom, Clark, Cotton-Schwab) that are used in deconvolution: deconvolution is often called "CLEANing"; model components identified during deconvolution are often called CLEAN components; and the final image is often called the CLEAN image.

## Inputs
- Visibilities (VisibilitySet): complex visibilities indexed by baseline, time, frequency and polarization
- UVW coordinates, weights, and flags (if present)
- Observation parameters: phase centre, frequency information, and time sampling
- Imaging configuration:
    - Image parameters (image size, pixel size/cell size, field of view)
    - Gridding configuration (kernel, oversampling/support, w-term handling)
    - Weighting scheme (natural / uniform / robust)
    - Deconvolution settings (algorithm choice, stopping criteria, masks)

## Outputs
Imaging produces one or more image products, including:

- Dirty image: the direct inverse transform of gridded visibilities.
- PSF (dirty beam): the image-plane response of the sampling pattern and weighting.
- Model image: a deconvolved estimate of the sky brightness.
- Residual image: dirty image minus the model convolved with the PSF.
- Restored image: model image convolved with a restoring beam plus residuals.

These may be produced as 2D images or image cubes (i.e. an image per frequency channel).

## Role
- Visualise the effect of array layout, observation parameters, measurement effects.
- Producing improved sky models during iterative self-calibration.
- Experiment with (and optimise) imaging and gridding settings and algorithms.
- Provide data for quality assurance and diagnostics that reveal sampling limitations and calibration errors.

## Invariants
- Imaging products are defined relative to a specific phase centre and image coordinate system.
- Image products share a common image grid (pixel size, shape, coordinate definition).
- The PSF corresponds to the same weighting and gridding choices used to form the dirty image.
- Residuals are computed by subtracting the model image convolved with the PSF from the dirty image.
- Imaging does not modify input visibilities.

## Related concepts
- [Imaging](imaging.md)
- [Sky Model](sky-model.md)
- [Telescope](telescope.md)
- [Predict](predict.md)
- [Corruptions](corruptions.md)
