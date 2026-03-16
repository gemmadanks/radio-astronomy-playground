"""Class for handling image processing tasks."""

import numpy as np

from starbox.visibility import VisibilitySet
from starbox.constants import SPEED_OF_LIGHT


class Imager:
    """Class for handling image processing."""

    def __init__(self, grid_size: int = 256, fov_deg: float = 5.0):
        """Initialize the Imager.

        Args:
            grid_size: Number of pixels along each image axis.
            fov_deg: Imaged field of view in degrees.
        """
        self.grid_size = grid_size
        self.fov_deg = fov_deg

    def grid(self, visibilities: VisibilitySet) -> np.ndarray:
        """
        Grid visibilities onto a regular uv grid using nearest-neighbour mapping,
        using all times and frequency channels.

        Notes:
          - Ignores w-term (small-field).
          - Uses uniform weighting (simple sum).
          - Adds Hermitian symmetric samples to encourage a real dirty image.
          - Grid is centered: DC is at (grid_size//2, grid_size//2).
        """
        grid = np.zeros((self.grid_size, self.grid_size), dtype=np.complex128)

        uvw_m = np.asarray(visibilities.uvw_m, dtype=float)  # (T,B,3)
        vis = np.asarray(visibilities.vis, dtype=np.complex128)  # (T,B,F)
        freqs = np.asarray(visibilities.freqs_hz, dtype=float)  # (F,)

        num_times, num_baselines, _ = uvw_m.shape
        num_channels = freqs.size

        half = self.grid_size // 2

        # Set uv scaling from requested image field-of-view.
        # Approximate relation: uv_max ~ N / (2 * FoV_rad).
        fov_rad = np.deg2rad(self.fov_deg)
        uv_max = self.grid_size / (2.0 * max(fov_rad, 1e-12))

        # Map uv in [-uv_max, uv_max] -> pixel in [0, grid_size-1]
        scale = (half - 1) / uv_max

        # Second pass: grid all samples
        for i in range(num_channels):
            lam = SPEED_OF_LIGHT / freqs[i]
            u = uvw_m[:, :, 0] / lam  # (T,B) wavelengths
            v = uvw_m[:, :, 1] / lam

            u_pix = np.rint(u * scale + half).astype(int)  # (T,B)
            v_pix = np.rint(v * scale + half).astype(int)

            for t_idx in range(num_times):
                vis_tb = vis[t_idx, :, i]  # (B,)
                up = u_pix[t_idx]
                vp = v_pix[t_idx]

                for b_idx in range(num_baselines):
                    ui = up[b_idx]
                    vi = vp[b_idx]

                    # Skip samples outside the imaged FoV
                    if abs(u[t_idx, b_idx]) > uv_max or abs(v[t_idx, b_idx]) > uv_max:
                        continue

                    if 0 <= ui < self.grid_size and 0 <= vi < self.grid_size:
                        val = vis_tb[b_idx]
                        grid[vi, ui] += val
                        # Hermitian symmetric point about the DC center (half, half)
                        sym_u = (2 * half - ui) % self.grid_size
                        sym_v = (2 * half - vi) % self.grid_size
                        grid[sym_v, sym_u] += np.conj(val)

        return grid

    def ifft(self, gridded_visibilities: np.ndarray) -> np.ndarray:
        """
        Inverse FFT uv-grid -> dirty image.
        Because the grid is centered (DC at center), use ifftshift before ifft2.
        """
        img = np.fft.ifft2(np.fft.ifftshift(gridded_visibilities))
        img = np.fft.fftshift(img)
        return np.real(img)

    def image(self, visibilities: VisibilitySet) -> np.ndarray:
        """Create an image from visibilities."""
        gridded_visibilities = self.grid(visibilities=visibilities)
        image = self.ifft(gridded_visibilities)
        return image
