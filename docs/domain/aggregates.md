# Domain model

This shows the core domain-driven-design (DDD) aggregates (groups of domain concepts treated as a unit) and domain services (performs domain operations) that are part of starbox.

## Aggregate roots
- Telescope
- Observation
- SkyModel

## Aggregates
- Station (inside Telescope)
- AntennaElement (inside Station)

## Value objects
- Site
- CalibrationConfig

## Strategies
- Corruption
- BeamModel

## Services
- CalibrationSolver
- VisibilityPredictor

## Derived artifacts
- VisibilitySet
- CalibrationSolution

```mermaid
classDiagram
    Telescope *-- Station
    Telescope --> Site
    Station *-- AntennaElement
    Station --> BeamModel

    VisibilityPredictor ..> Telescope
    VisibilityPredictor ..> Observation
    VisibilityPredictor ..> SkyModel

    Corruption <|-- StationGains
    Corruption <|-- ThermalNoise
    Corruption <|-- Bandpass
    Corruption <|-- PhaseScreen

    CalibrationSolver ..> VisibilitySet
    CalibrationSolver ..> CalibrationSolution
    CalibrationSolver ..> CalibrationConfig

    class Telescope{
        +string name
        +Site location
        +list~Station~ stations

        +baseline_station_pairs()
        +uvw(Observation)
        +plot()
        +hour_angle(Observation)
    }

    class Site{
        +float latitude_rad
        +float longitude_rad
        +float height_m
    }

    class Station{
      +string name
      +float diameter_m
      +tuple position_enu_m
      +BeamModel beam_model
      +list~AntennaElement~ antenna_elements
      +plot()
    }

    class AntennaElement{
      +tuple element_position_enu_m
      +float element_rotation_angle
    }

    class SkyModel{
        +string name
        +tuple phase_centre_rad
        +tuple fov_ra_dec_rad
        +nd.array ra_rad
        +nd.array dec_rad
        +nd.array flux_jy
        +nd.array alpha
        +sample_sources(max_flux, num_sources)
        +lmn(phase_centre_rad=None)
        +plot()
    }

    class Observation{
        +nd.array times_mjd
        +nd.array freqs_hz
        +tuple phase_centre_rad
    }

    class VisibilityPredictor{
        +predict_visibilities(telescope, observation, skymodel) VisibilitySet
    }

    class VisibilitySet{
        +nd.array visibilities
        +nd.array uvw_m
        +nd.array ant1
        +nd.array ant2
        +nd.array times_mjd
        +nd.array time_index
        +nd.array freqs_hz
        +nd.array weights
    }

    class CalibrationConfig{
        +string mode
        +float solint_time
        +float solint_freq
        +string ref_ant
        +float min_snr
        +int min_nvis
        +int max_iters
        +float tol
        +tuple clip_amp_range
        +string normalisation_policy
    }

    class CalibrationSolver{
        +solve(vis_obs, vis_model, calibration_config) CalibrationSolution
    }

    class CalibrationSolution{
        +nd.array gains
        +nd.array time_centres_mjd
        +nd.array freq_centres_hz
        +int ref_ant
        +nd.array flags
        +nd.array qa_metrics
        +evaluate()
        +apply(vis_obs) VisibilitySet
    }

    class BeamModel{
        +string name
        +voltage_response(l, m, freqs_hz, times_mjd)
    }

    class Corruption{
        +string name
        +bool enabled
        +apply(vis, telescope, observation) VisibilitySet
    }

```
