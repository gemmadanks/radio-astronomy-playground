# Glossary
## Observations
- Scan
- Calibrator
- Target

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
- [Sources](concepts/sky-model.md)
    - Point source
    - Extended source (*extended emission* or *gaussian blob*)
- [Source catalog](concepts/sky-model.md) (*source list*)
- [Sky model](concepts/sky-model.md)
- Apparent sky
- True sky
- Patches

### Modes
- Wideband
- Widefield
- Drift scan

### Units & quantities
- Jansky
- Radians
- Flux density (*flux*, *intensity* or *brightness*)

### Coordinates & axes
- Direction cosines (l,m,n)
- Baseline coordinates (u,v,w)
- Frequency
- Channel

## Telescope
- [Telescope](concepts/telescope.md)
- [Interferometer](concepts/telescope.md)
- [Baseline](concepts/telescope.md)
- [Antenna](concepts/telescope.md)
- Receptor
- Receiver
- Aperture
- Diameter

### Array configuration
- [Array](concepts/telescope.md)
- Sub-array
- [Layout](concepts/telescope.md)
- [uv-coverage](concepts/telescope.md)
- [Station](concepts/telescope.md)
- Sub-station
- Rigid rotation

## Interferometry
- VLBI
- Aperture synthesis
- Fringes
- Correlator
- Side lobes
- Delay

## Data processing

### Beam
- [Beam model](concepts/measurement-model.md)
- Beam forming
- [Primary beam](concepts/primary-beam.md)
- Tied-array beam forming
- Beam correction (*Applying the beam*)

### Calibration
- [Calibration](concepts/calibration.md)
- Jones matrix
- Solver
- Calibration solution (*solution*)
- Apply solutions
- [Predict](concepts/predict.md)

#### Modes
- Phase-only
- Amplitude and phase
- Direction-independent
- Direction-dependent
- [Self-calibration](concepts/self-calibration.md)
- Self-calibration cycle

#### Gains
- Gains
- Phase
- Amplitude
- [Complex gains](concepts/measurement-model.md)

#### Effects
- [Measurement model](concepts/measurement-model.md)
- [Corruptions](concepts/measurement-model.md)
- [Phase screen](concepts/measurement-model.md) (*TEC screen*)
- [Bandpass](concepts/measurement-model.md)
- [Direction-dependent effect](concepts/measurement-model.md) (DDE)

#### Control
- Flagging
- Reference antenna

### Imaging
- [Imaging](concepts/imaging.md)

#### Modes
- Continuum imaging
- Spectral imaging

#### Data products
- Artifacts
- [Dirty image](concepts/imaging.md)
- [Residual image](concepts/imaging.md)
- [Clean image](concepts/imaging.md) (*restored image*)
- [Model image](concepts/imaging.md)
- [Image cube](concepts/imaging.md)
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
- [Stokes parameters (I, Q, U, V)](concepts/stokes-parameters.md)

#### Deconvolution
- [Deconvolution](concepts/imaging.md)
- Briggs weighting
- [Model component](concepts/imaging.md) (*CLEAN component*)
- Major cycle
- Minor cycle
- [Point spread function](concepts/imaging.md) (PSF)
- FWHM
- First null

#### Concepts
- [Image plane](concepts/imaging.md)
- [Visibility plane](concepts/imaging.md) (*Fourier space*)

## Data formats
- Measurement set
- FITS file
- CASA table
- h5parm

## Algorithms
- W-stacking
- FFT
- [CLEAN](concepts/imaging.md)
- [Högbom CLEAN](concepts/imaging.md)
- [Multi-scale CLEAN](concepts/imaging.md)
- Radio Interferometry Measurement equation (RIME)
- [Gridding](concepts/imaging.md)
- Source finding
