# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['piontologyextractor', 'piontologyextractor.Extractor']

package_data = \
{'': ['*']}

install_requires = \
['jaal>=0.0.9,<0.0.10',
 'openpyxl>=3.0.7,<4.0.0',
 'pandas>=1.3.2,<2.0.0',
 'piauthorizer>=0.9.5,<0.10.0']

setup_kwargs = {
    'name': 'piontologyextractor',
    'version': '0.1.0',
    'description': 'A package that can deal with extracting useful info from our Graph Ontology.',
    'long_description': None,
    'author': 'David Berenstien',
    'author_email': 'david.berenstein@pandoraintelligence.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
