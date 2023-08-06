# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hbase', 'hbase.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2', 'uplink>=0.9.4']

setup_kwargs = {
    'name': 'hbase',
    'version': '1.0.0',
    'description': 'Hbase REST API client built using uplink',
    'long_description': '<h1 align="center">\n   <strong>hbase</strong>\n</h1>\n\n<p align="center">\n    <a href="https://codecov.io/gh/CapgeminiInventIDE/hbase" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/CapgeminiInventIDE/hbase?color=%2334D058" alt="Coverage">\n    </a>\n    <a href="https://CapgeminiInventIDE.github.io/hbase" target="_blank">\n        <img src="https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat" alt="Docs">\n    </a>\n    <a href="https://pypi.org/project/hbase/" target="_blank">\n        <img src="https://img.shields.io/pypi/v/hbase.svg" alt="PyPI Latest Release">\n    </a>\n    <br /><a href="https://github.com/CapgeminiInventIDE/hbase/blob/main/LICENSE" target="_blank">\n        <img src="https://img.shields.io/github/license/CapgeminiInventIDE/hbase.svg" alt="License">\n    </a>\n    <a href="https://github.com/psf/black" target="_blank">\n        <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">\n    </a>\n</p>\n\nHbase REST API client built using uplink\n\n## Main Features\n\n- A transparent and user friendly HBase REST API client\n- Easy to extend by subclassing and utilizing uplink\'s Consumer class\n- A great alternative to HBase Thrift client\n\n## Installation\n\n```console\n$ pip install hbase\n\n---> 100%\n```\n\n## Usage\n\nBuild an instance to interact with the web service, check out the [HBase client reference](reference/client.md) for a full list of available methods.\n\n```python\nfrom hbase import HBase\n\nhbase = HBase(base_url="http://localhost:8000")\n```\n\nThen, executing an HTTP request is as simply as invoking a method.\n\n```python\n# Get all rows using the wildcard, or supply exact row_id for single row\nhbase.get_row(table="example_table", row_id="*")\n```\n\nThe returned object is a friendly Pydantic model which will automatically decode the response from base64:\n\n```python\nCellSet(\n    Row=[\n        Row(\n            key="decoded_key", \n            Cell=[\n                Cell(\n                    column="decoded_column", \n                    timestamp=39082034, \n                    value="decoded_value"\n                ), \n                ...\n            ]\n        ), \n    ...]\n)\n```\n\nSimilarly you can perform other CRUD operations on HBase, such as inserting a row, note that the data will automatically be encoded into base64 for you free of charge!\n\n```python\nhbase.insert_rows(\n    test_table_name, \n    rows={\n        "row-1": {\n            "col1": "dat1", \n            "col2": "dat2"\n        }, \n        "row-2": {\n            "col1": "dat1", \n            "col2": "dat2"\n        }\n    }\n)\nhbase.insert_row(\n    test_table_name, \n    row_id="row-3", \n    column_data={\n        "col1": "dat1", \n        "col2": "dat2"\n    }\n)\n```\n\nFor sending non-blocking requests, HBase uses Uplink, which comes with support for aiohttp and twisted.\n\n## Credits\n\n- [Uplink](https://github.com/prkumar/uplink) - A Declarative HTTP Client for Python\n- [HBase REST API documentation](https://hbase.apache.org/1.2/apidocs/org/apache/hadoop/hbase/rest/package-summary.html) - Used to help build out the package\n\n## License\n\n- [Mozilla Public License Version](/LICENSE)\n',
    'author': 'Andy Challis',
    'author_email': 'andrewchallis@hotmail.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CapgeminiInventIDE/hbase',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
