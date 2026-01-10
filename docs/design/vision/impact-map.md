# Impact map

Calibration and imaging workflows in radio astronomy are complex, involving many interacting parameters and iterative decision-making. This expert knowledge must be encoded into production pipelines. This project is explicitly focused on building intuition for these processes, especially self-calibration, through controlled, interactive experiments and diagnostics.

The impact map below captures the main goal of the project and links it to who it is designed for (a learner of radio astronomy), the behavioural impacts we want to enable and the deliverable slices that support those impacts.

The map is not a fixed feature roadmap or a complete product specification. It is a tool for prioritising what to implement next and a way to keep development focused on learning outcomes. The map will evolve over time as experiments reveal misconceptions and incorrect assumptions.

```mermaid
flowchart LR
  subgraph GOALS[Goals]
    G1["Build intuition for self-calibration and imaging"]
  end

  subgraph ACTORS[Actors]
    A1["Radio Astronomy Learner"]
  end

  subgraph IMPACTS[Impacts]
    I1["Detect self-cal improvement vs overfitting"]
    I2["Diagnose causes of self-cal divergence"]
    I3["Interpret gain solutions for stability and plausibility"]
    I4["Relate uv coverage and residuals to image artefacts"]
    I5["Choose appropriate calibration parameters"]
    I6["Assess scientific image quality using multiple metrics"]
    I7["Recognise when beam/DDE effects dominate errors"]
  end

  subgraph SLICES[Deliverable Slices]
    S1["S1: Self-cal loop + diagnostics (MVP)"]
    S2["S2: Calibration parameter sweeps"]
    S3["S3: Imaging artefact lab"]
    S4["S4: Beam / DDE lab"]
  end

  G1 --> A1
  A1 --> I1 & I2 & I3 & I4 & I5 & I6 & I7

  I1 --> S1
  I2 --> S1
  I3 --> S1
  I4 --> S1

  I1 --> S2
  I2 --> S2
  I5 --> S2

  I4 --> S3
  I6 --> S3

  I7 --> S4

  S1 --> S2 --> S3 --> S4
```

### Minimum Viable Learning Loop (MVP)

The initial implementation focuses on **Slice S1: Self-cal loop + diagnostics**.
This slice establishes the minimal end-to-end loop required to:

1. Simulate sky model with 1-5 point sources
2. Simulate telescope, a few stations
3. Simulate observation, a few channels, a few hours
4. Predict visibilities from sky model, no w-term
5. Add phase-only corruptions and noise to visibilities
6. Solve for and apply calibration solutions
8. Image the result before and after calibration
9. Evaluate outcomes using multiple diagnostics

All subsequent slices depend on this loop. Features not directly supporting this slice are intentionally deferred.
