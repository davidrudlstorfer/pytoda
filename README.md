<h1 align="center">
  PyToDa 🐍🛠️
</h1>

<div align="center">

[![Pipeline](https://github.com/davidrudlstorfer/pytoda/actions/workflows/main_pipeline.yml/badge.svg)](https://github.com/davidrudlstorfer/pytoda/actions/workflows/main_pipeline.yml)
[![Documentation](https://github.com/davidrudlstorfer/pytoda/actions/workflows/main_documentation.yml/badge.svg)](https://davidrudlstorfer.github.io/pytoda/)
[![Coverage badge](https://github.com/davidrudlstorfer/pytoda/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/davidrudlstorfer/pytoda/tree/python-coverage-comment-action-data)

</div>

PyToDa (**Py**thon **To**ols for the **Da**ily Usage) provides useful tools for the day to day usage with the multi-physics simulation framework [4C](https://www.4c-multiphysics.org) and is based on [PySkel](https://github.com/davidrudlstorfer/pyskel). Currently the following tools are available:

- A 4C .dat input file formatter which beautifully formats the input file so all columns and numbers are aligned for easier readability.
- An arbitrary unit converter which can be very easily be included in other frameworks.
- A logging framework which can be easily included into other frameworks.

The remaining parts of the readme are structured as follows:

- [Installation](#installation)
- [Execution](#execution)
  - [.dat input file formatter](#dat-input-file-formatter)
  - [Unit converter](#unit-converter)
  - [Logger](#logger)
  - [Run testing framework and create coverage report](#run-testing-framework-and-create-coverage-report)
  - [Create documentation](#create-documentation)
- [Dependency Management](#dependency-management)
- [Contributing](#contributing)
- [License](#license)


## Installation

For a quick and easy start an Anaconda/Miniconda environment is highly recommended. Other ways to install PyToDa are possible but here the installation procedure is explained based on a conda install. After installing Anaconda/Miniconda
execute the following steps:

- Create a new Anaconda environment based on the [`environment.yml`](./environment.yml) file:
```
conda env create -f environment.yml
```

- Activate your newly created environment:
```
conda activate pytoda
```

- Install all PyToDa requirements with:
```
pip install -e .
```

- Finally, install the pre-commit hook with:
```
pre-commit install
```

Now you are up and running 🎉

## Execution

The following brief tutorials highlight how each tool can be used:

### .dat input file formatter

Simply call the .dat input file formatter with

```
format_dat --dat_file_path ../path/to/datfile.dat --output_file_path ../path/to/final/datfile.dat --format_sections NODE COORDS
```

If the output file path coincides with the input file path the original file simply gets overwritten. Additionally, you need to provide the sections which will be formatted.

### Unit converter

The unit converter can be called with

```
convert_unit --unit_length "m" --unit_weight "g" --unit_time "s" --quantity "1 bar"
```

by providing the base units for the target unit system. Finally, the provided quantity will be converted into the taret unit system.

### Logger

The logger can be simply included into any software framework by providing the [functions](/src/pytoda/logger.py) with the necessary arguments. An example for the logger usage can be found within [PySkel](https://github.com/davidrudlstorfer/pyskel).

### Run testing framework and create coverage report

To locally execute the tests and create the html coverage report simply run

```
pytest
```

### Create documentation

To locally create the documentation from the provided docstrings simply run

```
pdoc --html --output-dir docs src/
```

## Dependency Management

To ease the dependency update process [`pip-tools`](https://github.com/jazzband/pip-tools) is utilized. To create the necessary [`requirements.txt`](./requirements.txt) file simply execute

```
pip-compile --all-extras --output-file=requirements.txt requirements.in
````

To upgrade the dependencies simply execute

```
pip-compile --all-extras --output-file=requirements.txt --upgrade requirements.in
````

Finally, perforfmance critical packages such as Numpy and Numba are installed via conda to utilize BLAS libraries.

## Contributing

All contributions are welcome. See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for more information.

## License

This project is licensed under a MIT license. For further information check [`LICENSE.md`](./LICENSE.md).
