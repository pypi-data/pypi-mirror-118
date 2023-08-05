"""
Meteopy package : fake package to illustrate the organisation of a
python project.
"""

from .viewer import Viewer

__version__ = 1.3


def view(filename: str, step: int = 0) -> int:
    """Shows the contents of a given netcdf file

    :param filename: Given netcdf file's name
    :type filename: str
    :param step: Step to display, defaults to 0
    :type step: int, optional
    :return: Step displayed
    :rtype: int
    """
    return Viewer(filename).display(step)
