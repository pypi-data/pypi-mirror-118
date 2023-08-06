# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tex_engine']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tex-engine',
    'version': '0.1.2.1',
    'description': 'Template Engine X. Have fun with HTML',
    'long_description': '# TEX - Template Engine X\nThis is a small TemplateEngine for Python3. The original code comes from [AlexMic](https://github.com/alexmic/microtemplates)',
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
