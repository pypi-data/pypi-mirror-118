# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['merakitools']

package_data = \
{'': ['*']}

install_requires = \
['meraki>=1.12.0,<2.0.0', 'rich>=10.7.0,<11.0.0', 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['merakitools = merakitools.main:app']}

setup_kwargs = {
    'name': 'merakitools',
    'version': '0.1.3',
    'description': 'CLI tools for managing Meraki networks based on Typer',
    'long_description': '# merakitools\n\nCLI tools for managing Meraki networks based on Typer',
    'author': 'Billy Zoellers',
    'author_email': 'billy.zoellers@mac.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
