# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eospyo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eospyo',
    'version': '0.2.0',
    'description': 'Interact with EOSIO blockchain networks',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
