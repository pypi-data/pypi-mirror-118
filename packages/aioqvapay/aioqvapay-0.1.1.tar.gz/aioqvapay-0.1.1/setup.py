# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aioqvapay', 'aioqvapay.v1', 'aioqvapay.v1.models']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[speedups]>=3.7.4,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'aioqvapay',
    'version': '0.1.1',
    'description': 'Asynchronous non-official QvaPay client for asyncio and Python language.',
    'long_description': '# Asynchronous QvaPay client for Python\n\n[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)\n[![Test](https://github.com/leynier/aioqvapay/workflows/CI/badge.svg)](https://github.com/leynier/aioqvapay/actions?query=workflow%3ACI)\n[![codecov](https://codecov.io/gh/leynier/aioqvapay/branch/main/graph/badge.svg?token=Z1MEEL3EAB)](https://codecov.io/gh/leynier/aioqvapay)\n[![DeepSource](https://deepsource.io/gh/leynier/aioqvapay.svg/?label=active+issues)](https://deepsource.io/gh/leynier/aioqvapay/?ref=repository-badge)\n[![Version](https://img.shields.io/pypi/v/aioqvapay?color=%2334D058&label=Version)](https://pypi.org/project/aioqvapay)\n[![Last commit](https://img.shields.io/github/last-commit/leynier/aioqvapay.svg?style=flat)](https://github.com/leynier/aioqvapay/commits)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/leynier/aioqvapay)](https://github.com/leynier/aioqvapay/commits)\n[![Github Stars](https://img.shields.io/github/stars/leynier/aioqvapay?style=flat&logo=github)](https://github.com/leynier/aioqvapay/stargazers)\n[![Github Forks](https://img.shields.io/github/forks/leynier/aioqvapay?style=flat&logo=github)](https://github.com/leynier/aioqvapay/network/members)\n[![Github Watchers](https://img.shields.io/github/watchers/leynier/aioqvapay?style=flat&logo=github)](https://github.com/leynier/aioqvapay)\n[![Website](https://img.shields.io/website?up_message=online&url=https%3A%2F%2Fleynier.github.io/aioqvapay)](https://leynier.github.io/aioqvapay)\n[![GitHub contributors](https://img.shields.io/github/contributors/leynier/aioqvapay)](https://github.com/leynier/aioqvapay/graphs/contributors)\n\n[Asynchronous](https://docs.python.org/3/library/asyncio-task.html) **non-official** [QvaPay](https://qvapay.com) client for [asyncio](https://docs.python.org/3/library/asyncio.html) and [Python language](https://www.python.org). This library is still under development, the interface could be changed\n\n## Features\n\n* Response models with type hints annotated fully.\n* Also internal code have type hints annotated fully.\n* Asynchronous behavior thank you to [aiohttp](aiohttp.org).\n* Coverage 100%\n* Project collaborative and open source.\n\nFor a **synchronous** behavior, <https://pypi.org/project/qvapay> can be used.\n\nFor more information about **QvaPay API**, read the [QvaPay docs](https://qvapay.com/docs).\n',
    'author': 'Leynier Gutiérrez González',
    'author_email': 'leynier41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://leynier.github.io/aioqvapay',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.14,<4.0.0',
}


setup(**setup_kwargs)
