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
        if fov_deg <= 0:
            raise ValueError(f"fov_deg must be positive, got {fov_deg!r}")
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

        num_channels = freqs.size

        half = self.grid_size // 2
        center = (self.grid_size - 1) / 2.0

        # Set uv scaling from requested image field-of-view.
        # Approximate relation: uv_max ~ N / (2 * FoV_rad).
        fov_rad = np.deg2rad(self.fov_deg)
        uv_max = self.grid_size / (2.0 * max(fov_rad, 1e-12))

        # Map uv in [-uv_max, uv_max] linearly onto pixel indices [0, grid_size-1].
        # With this choice:
        #   u = -uv_max -> 0
        #   u =  0      -> ~ (grid_size - 1) / 2 (center)
        #   u = +uv_max -> grid_size - 1
        scale = (self.grid_size - 1) / (2.0 * uv_max)

        # Second pass: grid all samples
        # Vectorized over times and baselines for each channel.
        grid_flat = grid.ravel()
        for i in range(num_channels):
            lam = SPEED_OF_LIGHT / freqs[i]
            u = uvw_m[:, :, 0] / lam  # (T,B) wavelengths
            v = uvw_m[:, :, 1] / lam

            # Pixel coordinates for all times and baselines at this channel
            u_pix = np.rint(u * scale + center).astype(int)  # (T,B)
            v_pix = np.rint(v * scale + center).astype(int)

            # Flatten (T,B) -> (N,) where N = T * B
            u_flat = u.ravel()
            v_flat = v.ravel()
            up_flat = u_pix.ravel()
            vp_flat = v_pix.ravel()
            vis_flat = vis[:, :, i].ravel().astype(np.complex128)

            # Mask samples outside the imaged FoV in uv-space
            fov_mask = (np.abs(u_flat) <= uv_max) & (np.abs(v_flat) <= uv_max)

            # Mask samples with pixel coordinates outside the grid
            in_x = (up_flat >= 0) & (up_flat < self.grid_size)
            in_y = (vp_flat >= 0) & (vp_flat < self.grid_size)
            pix_mask = in_x & in_y

            # Combined validity mask
            mask = fov_mask & pix_mask
            if not np.any(mask):
                continue

            up_valid = up_flat[mask]
            vp_valid = vp_flat[mask]
            vals_valid = vis_flat[mask]

            # Linear indices into flattened grid for direct accumulation
            idx = vp_valid * self.grid_size + up_valid
            np.add.at(grid_flat, idx, vals_valid)

            # Hermitian symmetric points about the DC center (half, half)
            sym_u = (2 * half - up_valid) % self.grid_size
            sym_v = (2 * half - vp_valid) % self.grid_size
            sym_idx = sym_v * self.grid_size + sym_u

            # Avoid double-counting samples whose symmetric pixel is the same as the original
            self_sym_mask = sym_idx != idx
            if np.any(self_sym_mask):
                np.add.at(
                    grid_flat,
                    sym_idx[self_sym_mask],
                    np.conj(vals_valid[self_sym_mask]),
                )

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
