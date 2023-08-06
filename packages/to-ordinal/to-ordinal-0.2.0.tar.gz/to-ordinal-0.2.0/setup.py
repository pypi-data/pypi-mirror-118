# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['to_ordinal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'to-ordinal',
    'version': '0.2.0',
    'description': '',
    'long_description': '# python-to-ordinal',
    'author': 'Bernardo da Eira Duarte',
    'author_email': 'bernardoeiraduarte@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bernardoduarte/python-to-ordinal',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
