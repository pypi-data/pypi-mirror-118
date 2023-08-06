# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['guzzy']

package_data = \
{'': ['*'], 'guzzy': ['commands/*']}

entry_points = \
{'console_scripts': ['guzzy = guzzy:main']}

setup_kwargs = {
    'name': 'guzzy',
    'version': '0.1.3',
    'description': 'Interactive CLI git client inside fzf.',
    'long_description': None,
    'author': 'samedamci',
    'author_email': 'samedamci@disroot.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/samedamci/guzzy',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
