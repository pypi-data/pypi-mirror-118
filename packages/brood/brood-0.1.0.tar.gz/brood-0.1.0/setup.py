# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brood']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.20,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'gitignore-parser>=0.0.8,<0.0.9',
 'identify>=2.2.13,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'rich>=10.9.0,<11.0.0',
 'rtoml>=0.7.0,<0.8.0',
 'typer>=0.3.2,<0.4.0',
 'watchdog>=2.1.5,<3.0.0']

entry_points = \
{'console_scripts': ['brood = brood.main:app']}

setup_kwargs = {
    'name': 'brood',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Brood\n\n[![PyPI](https://img.shields.io/pypi/v/brood)](https://pypi.org/project/brood/)\n[![PyPI - License](https://img.shields.io/pypi/l/brood)](https://pypi.org/project/brood/)\n\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/JoshKarpel/brood/main.svg)](https://results.pre-commit.ci/latest/github/JoshKarpel/brood/main)\n[![codecov](https://codecov.io/gh/JoshKarpel/brood/branch/main/graph/badge.svg?token=2sjP4V0AfY)](https://codecov.io/gh/JoshKarpel/brood)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![GitHub issues](https://img.shields.io/github/issues/JoshKarpel/brood)](https://github.com/JoshKarpel/brood/issues)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/JoshKarpel/brood)](https://github.com/JoshKarpel/brood/pulls)\n',
    'author': 'Josh Karpel',
    'author_email': 'josh.karpel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JoshKarpel/brood',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
