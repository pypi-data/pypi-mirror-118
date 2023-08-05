"""
Viewer module used for viewing NetCDF files
"""

# Standard package
import argparse

# Third parties packages
import mflog
import xarray as xr
import matplotlib.pyplot as plt

# Own package
from meteopy.settings import LOGGER


class Viewer:
    """Class for viewing NetCDF file content

    :param filename: NetCDF file's name to open and view
    :type filename: str
    """

    def __init__(self, filename: str) -> None:
        self.filename = filename
        LOGGER.bind(filename=filename)
        LOGGER.debug("Trying to open given file")
        try:
            self.da = xr.open_dataarray(filename)
        except (ValueError, OSError):
            LOGGER.error("Failed to open given file", exc_info=True)
            self.da = xr.DataArray()
        LOGGER.info("File loaded.")

    def display(self, step: int = 0) -> int:
        """displays and shows given viewer's file content at the given step

        :param step: step to display, defaults to 0
        :type step: int, optional
        :return: step to display
        :rtype: int
        """
        LOGGER.debug("Displaying file.")
        self.da.isel(step=step).plot()
        plt.show()
        return step


if __name__ == "__main__":
    # Arguments parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Netcdf file to view")
    parser.add_argument("-s", "--step", type=int, default=0, help="Step to view")
    parser.add_argument(
        "-v", "--verbose", help="increase output verbosity", action="store_true"
    )
    args = parser.parse_args()
    if args.verbose:
        mflog.set_config(minimal_level="DEBUG")

    Viewer(args.filename).display(step=args.step)

    print(
        "displays and shows given viewer's file content at the given step :param step:"
        "step to display, defaults to 0 :type step: int, optional"
    )
