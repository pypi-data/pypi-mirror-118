# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['outlookcalendarsyncer']

package_data = \
{'': ['*']}

install_requires = \
['O365>=2.0.15,<3.0.0', 'dataclasses-json>=0.5.5,<0.6.0', 'tzlocal==2.1']

entry_points = \
{'console_scripts': ['outlookcalendarsyncer = '
                     'outlookcalendarsyncer.application:main']}

setup_kwargs = {
    'name': 'outlookcalendarsyncer',
    'version': '0.1.0',
    'description': '',
    'long_description': '# OutlookCalendarSyncer\n\n## How to setup dev environment\n\n### Prerequisites\n\nFollowing software is required to run spark application:\n\n* Python 3\n* [Poetry](https://python-poetry.org)\n* [Pyenv](https://github.com/pyenv/pyenv)\n\n### Run\n\n```shell\n# Install required python version\n$ pyenv install 3.9.6\n\n# Binding required python version to this directory\n$ pyenv local 3.9.6\n\n# Install poetry\n$ pip3 install poetry\n\n# Resolve dependencies\n$ poetry install\n\n# Check - all tests should pass\n$ poetry run pytest\n\n# Sync configured \n$ poetry run python -m outlookcalendarsyncer\n```\n\n## How to build package\n\n```shell\n$ poetry build\n```\n\n## How to test\n\n```shell\n$ poetry run pytest\n```\n',
    'author': 'Alnen',
    'author_email': 'uzhegov37@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MattiooFR/package_name',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
