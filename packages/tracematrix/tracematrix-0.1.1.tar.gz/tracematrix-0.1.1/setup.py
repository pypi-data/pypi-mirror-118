# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tracematrix', 'tracematrix.reporters']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tracematrix',
    'version': '0.1.1',
    'description': 'Tool to create a traceability matrix',
    'long_description': '# tracematrix\nPython tool to create a traceability matrix.\n',
    'author': 'Andreas Finkler',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
