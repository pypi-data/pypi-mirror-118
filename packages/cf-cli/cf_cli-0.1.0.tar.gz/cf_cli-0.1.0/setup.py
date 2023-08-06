# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cf_cli',
 'cf_cli.backend.endpoints',
 'cf_cli.backend.endpoints.token',
 'cf_cli.backend.endpoints.user',
 'cf_cli.backend.schemas',
 'cf_cli.cli',
 'cf_cli.cli.command_groups']

package_data = \
{'': ['*']}

install_requires = \
['orjson>=3.6,<4.0',
 'pydantic>=1.8,<2.0',
 'requests>=2.26,<3.0',
 'typer[all]>=0.4,<1.0']

entry_points = \
{'console_scripts': ['cloudflare = cf_cli:app']}

setup_kwargs = {
    'name': 'cf-cli',
    'version': '0.1.0',
    'description': 'Terminal interaction with Cloudflare',
    'long_description': '# Cloudflare CLI\nTerminal interaction with Cloudflare\n',
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
