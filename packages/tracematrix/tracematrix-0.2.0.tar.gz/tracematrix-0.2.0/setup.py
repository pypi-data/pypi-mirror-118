# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tracematrix', 'tracematrix.reporters']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'tracematrix',
    'version': '0.2.0',
    'description': 'Tool to create a traceability matrix',
    'long_description': '# tracematrix\nA Python tool to create a traceability matrix.\n\n## Scope\nThis package focuses on generating the traceability matrix itself.\nAs the APIs and export formats of different test management and/or requirement management tools can be very different, the data acquisition and conversion is not in the scope of this package. However, it aims to provide a convenient way to create the individual items (e.g. requirements, testcases or any other traceable item) and traces between them.\n\n## How to use this package\nCurrently it is only possible to use this package programmatically in your own script.\n\nAll traceable items have a unique ``id`` and a set of other items that they are traced to.\n\nTo get an existing or create a new item, you can use the class method ``get_by_id(id_)``.\nIt will only create a new instance if no existing item with this ``id`` could be found.\nThis means that you don\'t have to keep track if you already processed this item, because\nsome items could appear more than once in your data (i.e. a requirement could appear on multiple test cases).\n\n```python\nfrom tracematrix.item import TraceItem\n\nreq1 = TraceItem.get_by_id("REQ_1")\ntestcase1 = TraceItem.get_by_id("TC_1")\n```\n\nCreating links between to items is done by simply passing the two items to ``TraceItem.add_trace(first, second)``.\nThis will create a bidirectional link between these elements and update the ``traced_to`` attribute on both.\n\n```python\nTraceItem.add_trace(req1, testcase1)\n```\n\nCurrently two output formats are supported - CSV and HTML.\nDefault is CSV, but you can specify the reporter when creating the ``TraceabilityMatrix``:\n\n```python\nfrom tracematrix.reporters import HtmlReporter\n\nmatrix = TraceabilityMatrix(testcases, requirements, reporter=HtmlReporter)\nmatrix.create_matrix("RequirementsTraceabilityMatrix.html")\n```\n',
    'author': 'Andreas Finkler',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
