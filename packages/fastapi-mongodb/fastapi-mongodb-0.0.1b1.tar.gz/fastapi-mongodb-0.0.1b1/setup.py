# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mongodb']

package_data = \
{'': ['*']}

install_requires = \
['fastapi',
 'motor',
 'orjson',
 'pydantic[dotenv,email]',
 'pyjwt',
 'pymongo[tls,srv]']

setup_kwargs = {
    'name': 'fastapi-mongodb',
    'version': '0.0.1b1',
    'description': 'Snippets for FastAPI to work with MongoDB by Motor driver.',
    'long_description': '![GitHub](https://img.shields.io/github/license/KosT-NavySky/fastapi-mongodb)\n![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/Kost-NavySky/fastapi-mongodb/Python%20package/master)\n![GitHub last commit (branch)](https://img.shields.io/github/last-commit/kost-navysky/fastapi-mongodb/master)\n![Codecov](https://img.shields.io/codecov/c/github/kost-navysky/fastapi-mongodb)\n[![](https://img.shields.io/badge/code%20style-black-000000?style=flat)](https://github.com/psf/black)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mongodb)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-mongodb)\n![PyPI](https://img.shields.io/pypi/v/fastapi-mongodb)\n\n# fastapi-mongodb\n\n### ATTENTION!\nThe project is under development, so there is a possibility of breaking changes.\n\nWhen the key points in development are completed, I will take care of the documentation.\n\nThe project is built for a scalable solution between two excellent technologies (FastAPI and MongoDB)\n\n### dependencies:\n- python 3.9+\n- fastapi\n- motor\n- pymongo\n- pydantic\n- pyjwt\n- orjson\n',
    'author': 'Kostiantyn Salnykov',
    'author_email': 'kostiantyn.salnykov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KosT-NavySky/fastapi_mongodb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
