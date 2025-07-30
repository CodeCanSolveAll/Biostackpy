"""
Created on %(date)s
@author: CodeCanSolveAll
Description:
"""
#%%% packages
from pathlib import Path
import numpy as np
import h5py


#%%% class and function definition
class ImageStack:
    """
    HDF5-backed 3D (or 4D) image stack with lazy loading.
    Designed for very large biological image datasets.

    Parameters
    ----------
    filepath : str or Path
        Full path to the HDF5 file.
    mode : str, default="a"
        File mode: "r" (read), "r+" (read/write), "a" (read/write/create).

    Notes
    -----
    - Stores main dataset in 'data'
    - Dimensions are attached as HDF5 scales ('x', 'y', 'z', 't')
    - Lazy access: slices load on-demand
    """

    DIM_LABELS = ["z", "y", "x", "t"]  # zyx + optional time

    def __init__(self, filepath, mode="a"):
        self.filepath = Path(filepath)
        self.mode = mode
        self._file = h5py.File(self.filepath, mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def shape(self):
        return self._file["data"].shape

    @property
    def dtype(self):
        return self._file["data"].dtype

    def create(self, shape, dtype="int8", chunks=None, compression="gzip"):
        """Create a new dataset."""
        if "data" in self._file:
            del self._file["data"]

        if chunks is None:
            chunks = (1,) + shape[1:]  # efficient for z-slicing

        dset = self._file.create_dataset(
            "data",
            shape=shape,
            dtype=dtype,
            chunks=chunks,
            compression=compression,
        )

        # Add dimension scales
        for i, dim in enumerate(shape):
            label = self.DIM_LABELS[i]
            scale = self._file.create_dataset(label, data=np.arange(dim))
            scale.make_scale(label)
            dset.dims[i].attach_scale(scale)

        return dset

    def __getitem__(self, key):
        return self._file["data"][key]

    def __setitem__(self, key, value):
        self._file["data"][key] = value

    def get_dim(self, axis):
        label = self.DIM_LABELS[axis]
        return self._file[label][:]

    def set_dim(self, axis, values):
        label = self.DIM_LABELS[axis]
        self._file[label][:] = values

    def iter_frames(self, axis=0):
        """Iterate over frames along given axis (default: z)."""
        for i in range(self.shape[axis]):
            yield self[(slice(None),) * axis + (i,)]

    def to_numpy(self, max_size_mb=500):
        """Load into memory if size is reasonable."""
        size_mb = np.prod(self.shape) * np.dtype(self.dtype).itemsize / 1e6
        if size_mb > max_size_mb:
            raise MemoryError(
                f"Stack too large ({size_mb:.1f} MB). Use slicing instead."
            )
        return self._file["data"][:]

    def close(self):
        """Close the HDF5 file."""
        if self._file:
            self._file.close()
#%%% inputs

#%%% script

