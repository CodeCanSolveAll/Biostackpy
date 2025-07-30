#%%% packages
from pathlib import Path
import h5py


#%%% class and function definition
class AfsRicmStack:
    """
    Specialized image stack for AFS-RICM experiments.
    Stores a 3D stack (frames × y × x) with experiment metadata.

    Parameters
    ----------
    filepath : str or Path
        Path to the HDF5 file.
    mode : str, default="a"
        File mode: "r" (read), "r+" (read/write), "a" (read/write/create).

    Structure
    ---------
    /data             - image stack [frames, y, x]
    /time             - per-frame acquisition time [s]
    /acoustic_power   - per-frame acoustic power [%]
    attrs:
        resolution    - µm/pixel
        original_file - original raw filename
        position      - chamber position label
    """

    def __init__(self, filepath, mode="a"):
        self.filepath = Path(filepath)
        self.mode = mode
        self._file = h5py.File(self.filepath, mode)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create(self, n_frames, height, width, dtype="uint16",
               resolution=None, original_file=None, position=None):
        """Create a new AFS-RICM stack."""
        if "data" in self._file:
            del self._file["data"]

        dset = self._file.create_dataset(
            "data",
            shape=(n_frames, height, width),
            dtype=dtype,
            chunks=(1, height, width),  # efficient for time slicing
            compression="gzip"
        )

        # Per-frame metadata arrays
        self._file.create_dataset("time", shape=(n_frames,), dtype="float64")
        self._file.create_dataset("acoustic_power", shape=(n_frames,), dtype="float32")

        # Global metadata
        self._file.attrs["resolution"] = resolution
        self._file.attrs["original_file"] = original_file
        self._file.attrs["position"] = position

        return dset

    @property
    def shape(self):
        return self._file["data"].shape

    @property
    def dtype(self):
        return self._file["data"].dtype

    def __getitem__(self, idx):
        return self._file["data"][idx]

    def __setitem__(self, idx, value):
        self._file["data"][idx] = value

    def set_frame_metadata(self, frame_idx, time=None, acoustic_power=None):
        """Attach per-frame metadata."""
        if time is not None:
            self._file["time"][frame_idx] = time
        if acoustic_power is not None:
            self._file["acoustic_power"][frame_idx] = acoustic_power

    def get_frame_metadata(self, frame_idx):
        """Retrieve metadata for a specific frame."""
        return {
            "time": float(self._file["time"][frame_idx]),
            "acoustic_power": float(self._file["acoustic_power"][frame_idx]),
        }

    def global_metadata(self):
        """Return a dict with global metadata."""
        return {
            "resolution": self._file.attrs.get("resolution"),
            "original_file": self._file.attrs.get("original_file"),
            "position": self._file.attrs.get("position"),
        }

    def iter_frames(self):
        """Yield (frame, metadata) tuples."""
        for i in range(self.shape[0]):
            yield self[i], self.get_frame_metadata(i)

    def close(self):
        if self._file:
            self._file.close()
            
#%%% inputs

#%%% script

