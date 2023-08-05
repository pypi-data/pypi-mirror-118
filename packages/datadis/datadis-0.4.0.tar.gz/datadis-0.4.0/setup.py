# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadis']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'datadis',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'Alvaro Tinoco',
    'author_email': 'alvarotinocomarmol@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
