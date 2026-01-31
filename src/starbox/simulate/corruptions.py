"""A class for simulating corruptions."""

from dataclasses import dataclass, field
import numpy as np

from starbox.visibility import VisibilitySet


@dataclass(slots=True)
class CorruptionsSpec:
    """A specification for signal corruptions.

    Attributes:
        rms_noise: The RMS noise level to add to the visibilities.
        rms_phase_gain: Phase gain errors for each station.
    """

    seed: int = 42
    rms_noise: float | None = None
    rms_phase_gain: float | None = None


@dataclass(slots=True)
class Corruptions:
    """A class representing corruptions to apply to a signal.

    Attributes:
        rms_noise: The RMS noise level to add to the visibilities.
        station_phase_gain: Phase gain errors for each station.
    """

    seed: int = 42
    rms_noise: float | None = None
    sigma: float | None = None
    rms_phase_gain: float | None = None
    rng: np.random.Generator = field(init=False, repr=False)
    spec: CorruptionsSpec | None = None

    def __post_init__(self):
        self.rng = np.random.default_rng(self.seed)
        if self.rms_noise is not None:
            self._add_noise(self.rms_noise)

    @classmethod
    def from_spec(cls, spec: CorruptionsSpec) -> "Corruptions":
        """Create a Corruptions instance from a CorruptionsSpec."""
        return cls(
            seed=spec.seed,
            rms_noise=spec.rms_noise,
            rms_phase_gain=spec.rms_phase_gain,
            spec=spec,
        )

    def _add_noise(self, rms_noise: float = 1.0):
        """Add Gaussian noise corruption."""
        self.rms_noise = rms_noise
        self.sigma = rms_noise / np.sqrt(2)

    def add_station_phase_gain(self, rms_phase_gain: float | None):
        """Add or update station phase gain corruption.

        Args:
            rms_phase_gain: The RMS of the station phase gain errors to apply.
                If a float is provided, random station phase gains with this RMS
                will be applied when :meth:`apply` is called. If ``None`` is
                provided, station phase gain corruption is disabled (i.e. no
                phase gain corruption will be applied).
        """
        self.rms_phase_gain = rms_phase_gain

    def apply(self, visibility_set: VisibilitySet) -> VisibilitySet:
        """Apply the corruptions to the given visibilities."""
        corrupted_visibility_set = VisibilitySet(
            vis=np.copy(visibility_set.vis),
            uvw_m=visibility_set.uvw_m,
            station1=visibility_set.station1,
            station2=visibility_set.station2,
            times_mjd=visibility_set.times_mjd,
            freqs_hz=visibility_set.freqs_hz,
            weights=visibility_set.weights,
        )
        if self.rms_phase_gain is not None:
            station_phase_gains = self._sample_station_phase_gains(
                num_stations=visibility_set.num_stations
            )
            corrupted_visibility_set = self._apply_station_phase_gain(
                corrupted_visibility_set, station_phase_gains
            )

        if self.sigma is not None:
            corrupted_visibility_set = self._apply_noise(corrupted_visibility_set)

        return corrupted_visibility_set

    def _apply_station_phase_gain(
        self, visibility_set: VisibilitySet, station_phase_gains: np.ndarray
    ) -> VisibilitySet:
        """Apply only the station phase gain corruption to the given visibilities."""

        phase_gains_1 = station_phase_gains[visibility_set.station1]
        phase_gains_2 = station_phase_gains[visibility_set.station2]
        # Broadcast station gains to all times and channels
        phase_gains_1 = phase_gains_1[np.newaxis, :, np.newaxis]
        phase_gains_2 = phase_gains_2[np.newaxis, :, np.newaxis]
        visibility_set.vis *= phase_gains_1 * np.conj(phase_gains_2)

        return visibility_set

    def _sample_station_phase_gains(self, num_stations: int) -> np.ndarray:
        """Sample random phase gains for each station."""
        if self.rms_phase_gain is None:
            raise ValueError("RMS phase gain is not set.")
        phi = self.rng.normal(loc=0.0, scale=self.rms_phase_gain, size=num_stations)
        # Reference station to have zero phase gain
        ref_station = 0
        phi[ref_station] = 0.0

        station_phase_gains = np.exp(1j * phi)
        return station_phase_gains

    def _apply_noise(self, visibility_set: VisibilitySet) -> VisibilitySet:
        """Apply only the noise corruption to the given visibilities."""
        if self.sigma is None:
            raise ValueError("Sigma for noise is not set.")
        noise_real = self.rng.normal(scale=self.sigma, size=visibility_set.vis.shape)
        noise_imag = self.rng.normal(scale=self.sigma, size=visibility_set.vis.shape)
        noise = noise_real + 1j * noise_imag
        visibility_set.vis += noise

        return visibility_set
