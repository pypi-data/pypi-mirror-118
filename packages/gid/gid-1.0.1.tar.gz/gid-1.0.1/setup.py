# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gid']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gid',
    'version': '1.0.1',
    'description': 'Gid is a small library for generating short globally unique, sortable uri safe identifiers.',
    'long_description': "# Gid <br> [![Release](https://github.com/kodemore/gid/actions/workflows/release.yml/badge.svg)](https://github.com/kodemore/gid/actions/workflows/release.yml) [![Linting and Tests](https://github.com/kodemore/gid/actions/workflows/main.yaml/badge.svg)](https://github.com/kodemore/gid/actions/workflows/main.yaml) [![codecov](https://codecov.io/gh/kodemore/gid/branch/main/graph/badge.svg?token=N6AROCAN9S)](https://codecov.io/gh/kodemore/gid) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\nGid is a small library for generating short globally unique, sortable uri safe identifiers.\n\n## Features\n- Generated ids are sortable\n- Generated ids carry creation time expressed in microseconds\n- Generated ids are globally unique\n- Minimal footprint\n- High performance\n\n\n## Installation\n\nWith pip,\n```shell\npip install gid\n```\nor through poetry\n```shell\npoetry add gid\n```\n\n## Example ids\n\n```\nShmX2HaaUB9UQL02 \nShmX2JGvSk4ZyZ13 \nShmX2Ku8mDizRc23 \nShmX2MWQVL5J7022 \nShmX2OCegs4MdP22 \nShmX2Pu2MDVFHa02 \nShmX2RYngGET4Z32 \nShmX2TCM6v701q23 \nShmX2UrBjxNGYM11\n```\n\n# Usage\n\n## Generating id\n```python\nfrom gid import Guid\n\nsome_id = Guid()\nsome_id.timestamp # contains timestamp expressed in milliseconds\nstr(some_id) # can be cast to a string\n```\n\n## Recreating id from string\n```python\nfrom gid import Guid\nmy_id = Guid()\n\nsame_id = Guid(str(my_id))\n\nassert same_id == my_id\nassert same_id.timestamp == my_id.timestamp\n```\n\n# Id structure\nGenerated identifiers are case-sensitive, which means string functions (like lowercase or uppercase) on generated \nidentifiers may break it because `Sbt5LrD9iSAwb300` is not the same value as `Sbt5LrD9iSAwB300`.\n\nThe below diagram represents single identifier's structure, which is 16-character long:\n```\n    Sbt5LrD9iSAwb300\n    |      |      |\n    +- first 7 characters for millisecond timestamp\n           |      |\n           +- next 7 characters is randomly generated hash\n                  |\n                  + last two characters to ensure uniqueness of guid in a single millisecond\n```\n\n> Within 1 ms there can be (62^2 - 620) unique generated ids on a single machine.\n",
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kodemore/gid',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
