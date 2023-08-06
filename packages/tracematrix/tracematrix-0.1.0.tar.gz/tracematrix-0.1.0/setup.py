# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tracematrix']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tracematrix',
    'version': '0.1.0',
    'description': 'Tool to create a traceability matrix',
    'long_description': None,
    'author': 'Andreas Finkler',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
