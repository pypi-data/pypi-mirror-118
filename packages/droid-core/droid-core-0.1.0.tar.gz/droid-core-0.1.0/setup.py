# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['droid_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'droid-core',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Leorio Paradinight',
    'author_email': '62891774+code-rgb@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
