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
    'version': '0.1.0',
    'description': 'Cloudflare interaction in a black box!',
    'long_description': '# Welcome to Cloudflare CLI\n\n> Cloudflare interaction in a black box!\n\nCloudflare CLI is the next Command Line Interface made for interacting with Cloudflare through the terminal!',
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
