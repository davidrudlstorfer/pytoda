<h1 align="center">
  PyToDa 🐍🛠️
</h1>

<div align="center">

[![Pipeline](https://github.com/davidrudlstorfer/pytoda/actions/workflows/main_pipeline.yml/badge.svg)](https://github.com/davidrudlstorfer/pytoda/actions/workflows/main_pipeline.yml)
[![Documentation](https://github.com/davidrudlstorfer/pytoda/actions/workflows/main_documentation.yml/badge.svg)](https://davidrudlstorfer.github.io/pytoda/)
[![Coverage badge](https://github.com/davidrudlstorfer/pytoda/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/davidrudlstorfer/pytoda/tree/python-coverage-comment-action-data)

</div>

PyToDa provides Python Tools for the daily usage including:

- A 4C .dat input file formatter
- TBD

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
- All necessary third party libraries can be installed using:
```
pip install -e .
```
- Finally, install the pre-commit hook with:
```
pre-commit install
```

Now you are up and running 🎉

## Execution

TBD

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
