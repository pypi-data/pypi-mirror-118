# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jrtimeman']

package_data = \
{'': ['*']}

install_requires = \
['beautiful-date>=2',
 'gcsa>=1.2',
 'google>=3.0',
 'matplotlib>=3.0',
 'numpy>=1.19',
 'pandas>=1']

setup_kwargs = {
    'name': 'jrtimeman',
    'version': '0.0.1',
    'description': 'Jumping Rivers: Time Management',
    'long_description': None,
    'author': 'Jack',
    'author_email': 'jack@jumpingrivers.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
