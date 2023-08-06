# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mgp']
setup_kwargs = {
    'name': 'mgp',
    'version': '0.1.1',
    'description': "Memgraph's module for developing MAGE modules. Used only for type hinting!",
    'long_description': None,
    'author': 'MasterMedo',
    'author_email': 'mislav.vuletic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
