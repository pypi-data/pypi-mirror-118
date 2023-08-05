# Meteopy

Meteopy is a phony package created to illustrate the organization of a python project (from environment and package management to distribution).

Meteopy allows you to watch netcdf files content :

```python
>>> import meteopy
>>> meteopy.view("my_file.nc")
```

## Installation

### Quick installation

To install Meteopy, simply : 
```bash
$ pip install meteopy
```
**Dependencies :** Meteopy depends on `xarray` and `matplotlib`.

### Dev installation

To use Meteopy in dev-mode :
```bash
$ git clone https://git.meteo.fr/deep_learning/demo-projet-python.git
$ cd demo-projet-python
$ make install
```
**Dependencies :** Dev-mode relies on conda for package and environment management.


## Documentation

This section explains the choices made to manage this phony project.

### Source code

This is the tree of the repository
.
├── .condarc                : conda configuration file
├── .gitignore              : list of file for git  to ignore
├── .gitlab-ci.yml          : gitlab CI's script
├── environment.yml         : conda environment configuration file
├── Makefile                : Makefile gathering install and updates command
├── mf.crt                  : Météo-France's certificate (used for publication)
├── README.md               : Documentation
├── requirements.txt        : libraries to install through pip
├── setup.py                : script used for distributing meteopy package
├── **example**             : directory containing examples
│   └── FF__HAUTEUR10.nc    : example file
├── **meteopy**             : package's main directory
│   ├── \__init\__.py       : initialisation module
│   ├── settings.py         : settings module
│   └── viewer.py           : viewer module
└── **tests**               : tests directory
    └── test_viewer.py      : script for testing the viewer module


### Environment

We use conda for environment management.

As you may see in the `create_env` command of the Makefile, the creation of the `meteopy-env` consists in the following commands :
1. Creation of the environment through : `conda env create -n meteopy-env --file environment.yml`
2. Activation of the environment using a simily `conda activate meteopy-env`
3. Installation of the remaining libraries (the ones not available on conda) using pip : `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt`
4. Eventually, the installation of the meteopy package in dev mode : `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -e .`

**Note :** here in MF, due to certificates restrictions, you should primarly use [Nexus](http://confluence.meteo.fr/display/MOT/Nexus+-+Guide+d%27utilisation) for package installations (conda and pip).
If some packages are not available on Nexus, then you can use the usual channels by avoiding the certificate restrictions :
- on conda : running the following command `conda config --set ssl_verify false` before conda usage.
- on pip : using the flags `--trusted-host pypi.org --trusted-host files.pythonhosted.org` in your commands.


### Packages

In this project, we use the following packages
* black : for linting
* flake8 : for linting
* matplotlib : for plotting and showing contents
* pytest : for unit testing
* mflog : for logging
* xarray : for handling netcdf files


### Distribution

Before distributing your package, you should have an accound on [pypi.org](pypi.org) (or on Nexus). You may configure where you want to upload your package using a .pypirc file in your $HOME directory.

The distribution is done using twine :
```
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org twine
python setup.py sdist bdist_wheel
twine upload --cert mf.crt dist/*
```

Here we use the `--cert` flag for specifying MF's certificate.

### CI/CD

We have two stages in the CI :
* test : it installs and tests the package (it is done every push)
* distrib : it distributes the package to pypi.org (only when merged into the master branch)
