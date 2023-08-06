# OutlookCalendarSyncer

## How to setup dev environment

### Prerequisites

Following software is required to run spark application:

* Python 3
* [Poetry](https://python-poetry.org)
* [Pyenv](https://github.com/pyenv/pyenv)

### Run

```shell
# Install required python version
$ pyenv install 3.9.6

# Binding required python version to this directory
$ pyenv local 3.9.6

# Install poetry
$ pip3 install poetry

# Resolve dependencies
$ poetry install

# Check - all tests should pass
$ poetry run pytest

# Sync configured 
$ poetry run python -m outlookcalendarsyncer
```

## How to build package

```shell
$ poetry build
```

## How to test

```shell
$ poetry run pytest
```
