# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slant']

package_data = \
{'': ['*'], 'slant': ['dictionaries/*']}

install_requires = \
['multiprocess>=0.70.12,<0.71.0', 'numpy>=1.19.5,<2.0.0']

setup_kwargs = {
    'name': 'slant',
    'version': '0.1.0',
    'description': 'Identify and quantify bias in Python',
    'long_description': None,
    'author': 'William W. Marx',
    'author_email': 'null@marx.design',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
