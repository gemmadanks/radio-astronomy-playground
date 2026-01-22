"""Class for handling image processing tasks."""

import numpy as np


class Imager:
    def __init__(self):
        self.grid_size = 256  # Example grid size

    def grid(self, visibilities):
        """Grid the visibilities onto a regular grid."""
        gridded_visibilities = np.ones((self.grid_size, self.grid_size), dtype=complex)

        return gridded_visibilities

    def fft(self, gridded_visibilities):
        """Convert visibilities to an image using a simple Fourier Transform."""

        # Assuming gridded visibilities is a 2D numpy array
        image = np.fft.ifft2(gridded_visibilities)
        image = np.fft.fftshift(image)
        return np.abs(image)

    def image(self, visibilities) -> np.ndarray:
        """Create an image from visibilities."""
        gridded_visibilities = self.grid(visibilities=visibilities)
        image = self.fft(gridded_visibilities)
        return image
