# Key concepts

The following is a list of common terms used in the radio astronomy domain. Key concepts that form the ubiquitous language for starbox have links with further details. This is a living document and will be updated as code is added.

## Observations
- [Observation](observation.md)
- **Scan**: A contiguous time interval during which the telescope observes a single field with fixed pointing.
- **Calibrator**: A source observed primarily to estimate instrumental or propagation effects.
- **Target**: A source or field observed for scientific analysis.

### Pointing
- Pointing
- Right ascension
- Declination
- Hour angle
- Integration time
- Phase centre

### Sky and signals
- Polarization
- Faraday rotation
- RFI
- [**Sources**]: sources of radio emission in a sky model or image.
    - Point source
    - Extended source (*extended emission* or *gaussian blob*)
- [**Sky model**](sky-model.md) (*source catalog*, *source list*)
- **Apparent sky**: The sky brightness distribution as modified by instrumental and propagation effects.
- **True sky**: The intrinsic sky brightness distribution, independent of the instrument.
- **Patches**: Groups of sky model components treated together, typically for direction-dependent calibration.

### Modes
- Wideband
- Widefield
- Drift scan

### Units & quantities
- Jansky
- Flux density (*flux*, *intensity* or *brightness*)

### Coordinates & axes
- Direction cosines (l,m,n)
- Baseline coordinates (u,v,w)

## Telescope
- [**Telescope**](telescope.md) (*interferometer*, *array*, *sub-array*, *station*, *sub-station*)
- [**Antenna**](telescope.md) (*receptor*, *receiver*)
- Aperture

### Array configuration
- [**uv-coverage**](telescope.md)
- [**Baseline**](telescope.md)
- Rigid rotation

## Interferometry
- VLBI
- Aperture synthesis
- Fringes
- Correlator
- Delay

## Data processing

### Beam
- [**Beam model**](beam-model.md) (*primary beam*)
- Beam forming
- Tied-array beam forming
- Side lobes

### Calibration
- **Calibration solution** (*solution*): An estimated set of parameters that can be applied to visibilities to correct for corruptions introduced by the hardware, electronics, atmosphere or thermal noise.
- **Reference antenna**: A station used to fix phase and amplitude degeneracies during calibration.
- **Calibration**: The process of estimating and applying calibration solutions.
- Jones matrix
- **Solver**: The algorithm used to estimate calibration solutions.
- [**Predict**](predict.md): The process of predicting ideal visibilities from sky model components.
- **Self-calibration cycle**: An iterative loop of imaging, model update, and calibration.

#### Modes
- Phase-only
- Amplitude and phase
- Direction-independent
- Direction-dependent
- Self-calibration (*self-calibration cycle*)

#### Gains
- Phase
- Amplitude
- [Complex gains](corruptions.md)

#### Effects
- [Corruptions](corruptions.md)
    - Phase screen (*TEC screen*)
    - Bandpass
    - Delay
    - Direction-dependent effect (DDE)

#### Control
- Flagging
- Reference antenna

### Imaging
- [Imaging](imaging.md)

#### Modes
- Continuum imaging
- Spectral imaging

#### Data products
- Artifacts
- Images
    - Dirty image
    - Residual image
    - Clean image (*restored image*)
    - Model image
- **Image cube**: one image per frequency channel stacked together.
- Spectral index map

#### Quality Metrics
- SNR
- Dynamic range

#### Wide-field
- Facet
- Sector
- Field
- W-term

#### Polarization
- Stokes parameters (I, Q, U, V)

#### Deconvolution
- [Deconvolution](imaging.md)
- Briggs weighting
- Model component (*CLEAN component*)
- Major cycle
- Minor cycle
- [Point spread function](imaging.md) (PSF)
- FWHM
- First null

#### Concepts
- Image plane (*image space*, *pixel space*)
- Visibility plane (*visibility space*, *Fourier space*)

## Data formats
- Measurement set
- FITS file
- CASA table
- h5parm

## Algorithms
- W-stacking
- [CLEAN](imaging.md)
- [Högbom CLEAN](imaging.md)
- [Multi-scale CLEAN](imaging.md)
- Radio Interferometry Measurement equation (RIME)
- [Gridding](imaging.md)
- Source finding
