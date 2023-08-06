# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysheller']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pysheller',
    'version': '0.1.1',
    'description': 'Small library to create Python application based on shell scripts.',
    'long_description': None,
    'author': 'samedamci',
    'author_email': 'samedamci@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/samedamci/guzzy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9.2,<4.0.0',
}


setup(**setup_kwargs)
