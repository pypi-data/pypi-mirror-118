# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tex_engine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tex-engine',
    'version': '0.1.0',
    'description': 'Template Engine X. Have fun with HTML',
    'long_description': None,
    'author': 'Leo B.',
    'author_email': 'bernerdoodle@outlook.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
