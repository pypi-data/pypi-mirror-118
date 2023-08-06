# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudflarectl', 'cloudflarectl.cli', 'cloudflarectl.cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.6,<4.0',
 'pydantic>=1.8,<2.0',
 'requests>=2.26,<3.0',
 'typer[all]>=0.4,<1.0']

entry_points = \
{'console_scripts': ['cloudflare = cloudflare_cli:CLI']}

setup_kwargs = {
    'name': 'cloudflarectl',
    'version': '0.0.1',
    'description': 'Cloudflare interaction in a black box!',
    'long_description': "# Greetings from `cloudflarectl`!\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/doublevcodes/cloudflarectl/Lint?label=Lint&logo=github)\n![PyPI](https://img.shields.io/pypi/v/cloudflarectl?label=PyPI&logo=pypi&logoColor=white)\n\n`cloudflarectl` is a command line interface constructed especially for interacting with Cloudflare.\nIt's interacting with Cloudflare within a black box; your terminal!\n",
    'author': 'Vivaan Verma',
    'author_email': 'vivaan.verma@gmail.com',
    'maintainer': 'Vivaan Verma',
    'maintainer_email': 'vivaan.verma@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
