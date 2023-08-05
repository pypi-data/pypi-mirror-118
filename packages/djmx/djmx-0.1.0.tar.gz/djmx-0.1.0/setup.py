# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djmx']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.6,<4.0.0']

setup_kwargs = {
    'name': 'djmx',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
