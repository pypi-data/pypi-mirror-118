# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['classification_service']

package_data = \
{'': ['*']}

install_requires = \
['flask']

setup_kwargs = {
    'name': 'classification-service',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'pvasisht',
    'author_email': 'prajwal_prakashvasisht@intuit.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
