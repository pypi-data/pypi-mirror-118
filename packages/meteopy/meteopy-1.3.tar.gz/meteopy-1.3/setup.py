import os
import setuptools


def get_version() -> str:
    """returns current version of the project

    :return: Current version of the project
    :rtype: str
    """
    init_filename = os.path.join(os.path.dirname(__file__), "meteopy", "__init__.py")
    with open(init_filename, "r") as fp:
        version_line = next(
            line for line in fp.readlines() if line.startswith("__version__ =")
        )
    return version_line.split()[-1]


setuptools.setup(
    name="meteopy",
    version=get_version(),
    author="LabIA-MF",
    author_email="lab_ia@meteo.fr",
    description="Code for MeteoPy project (demo project)",
    url="https://git.meteo.fr/deep_learning/demo-projet-python",
    packages=setuptools.find_packages(),
)
