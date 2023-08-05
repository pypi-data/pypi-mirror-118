<!--
<p align="center">
  <img src="https://github.com/biolookup/biolookup/raw/main/docs/source/logo.png" height="150">
</p>
-->

<h1 align="center">
  Biolookup
</h1>

<p align="center">
    <a href="https://github.com/biolookup/biolookup/actions?query=workflow%3ATests">
        <img alt="Tests" src="https://github.com/biolookup/biolookup/workflows/Tests/badge.svg" />
    </a>
    <a href="https://github.com/cthoyt/cookiecutter-python-package">
        <img alt="Cookiecutter template from @cthoyt" src="https://img.shields.io/badge/Cookiecutter-python--package-yellow" /> 
    </a>
    <a href="https://pypi.org/project/biolookup">
        <img alt="PyPI" src="https://img.shields.io/pypi/v/biolookup" />
    </a>
    <a href="https://pypi.org/project/biolookup">
        <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/biolookup" />
    </a>
    <a href="https://github.com/biolookup/biolookup/blob/main/LICENSE">
        <img alt="PyPI - License" src="https://img.shields.io/pypi/l/biolookup" />
    </a>
    <a href='https://biolookup.readthedocs.io/en/latest/?badge=latest'>
        <img src='https://readthedocs.org/projects/biolookup/badge/?version=latest' alt='Documentation Status' />
    </a>
    <a href="https://zenodo.org/badge/latestdoi/400996921">
        <img src="https://zenodo.org/badge/400996921.svg" alt="DOI">
    </a>
    <a href='https://github.com/psf/black'>
        <img src='https://img.shields.io/badge/code%20style-black-000000.svg' alt='Code style: black' />
    </a>
</p>

Get metadata and ontological information about biomedical entities.

### 🕸️ Lookup App

After installing with the `[web]` extras, you can run the lookup app in local mode with:

```shell
$ biolookup web --lazy
```

This means that the in-memory data from `pyobo` are used. If you have a large external database, you
can run in remote mode with the `--sql` flag:

```shell
$ biolookup web --sql --uri postgresql+psycopg2://postgres:biolookup@localhost:5434/biolookup
```

If `--uri` is not given for the `web` subcommand, it
uses `pystow.get_config("pyobo", "sqlalchemy_uri)`to look up from `PYOBO_SQLALCHEMY_URI` or
in `~/.config/pyobo.ini`. If none is given, it defaults to a SQLite database
in `~/.data/pyobo/pyobo.db`.

### 🗂️ Load the Database

```shell
$ biolookup load  --uri postgresql+psycopg2://postgres:biolookup@localhost:5434/biolookup
```

If `--uri` is not given for the `load` subcommand, it
uses `pystow.get_config("pyobo", "sqlalchemy_uri)` to look up from `PYOBO_SQLALCHEMY_URI` or
in `~/.config/pyobo.ini`. If none is given, it defaults to a SQLite database
in `~/.data/pyobo/pyobo.db`.

## 🚀 Installation

The most recent release can be installed from
[PyPI](https://pypi.org/project/biolookup/) with:

```bash
$ pip install biolookup
```

The most recent code and data can be installed directly from GitHub with:

```bash
$ pip install git+https://github.com/biolookup/biolookup.git
```

To install in development mode, use the following:

```bash
$ git clone git+https://github.com/biolookup/biolookup.git
$ cd biolookup
$ pip install -e .
```

## 👐 Contributing

Contributions, whether filing an issue, making a pull request, or forking, are appreciated. See
[CONTRIBUTING.rst](https://github.com/biolookup/biolookup/blob/master/CONTRIBUTING.rst) for more
information on getting involved.

## 👀 Attribution

### ⚖️ License

The code in this package is licensed under the MIT License.

<!--
### 📖 Citation

Citation goes here!
-->

### 🎁 Support

The Biolookup Service was developed by the [INDRA Lab](https://indralab.github.io), a part of the
[Laboratory of Systems Pharmacology](https://hits.harvard.edu/the-program/laboratory-of-systems-pharmacology/about/)
and the [Harvard Program in Therapeutic Science (HiTS)](https://hits.harvard.edu)
at [Harvard Medical School](https://hms.harvard.edu/).

### 💰 Funding

This project has been supported by the following grants:

| Funding Body                                             | Program                                                                                                                       | Grant           |
|----------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|-----------------|
| DARPA                                                    | [Automating Scientific Knowledge Extraction (ASKE)](https://www.darpa.mil/program/automating-scientific-knowledge-extraction) | HR00111990009   |

### 🍪 Cookiecutter

This package was created with [@audreyfeldroy](https://github.com/audreyfeldroy)'s
[cookiecutter](https://github.com/cookiecutter/cookiecutter) package
using [@cthoyt](https://github.com/cthoyt)'s
[cookiecutter-snekpack](https://github.com/cthoyt/cookiecutter-snekpack) template.
