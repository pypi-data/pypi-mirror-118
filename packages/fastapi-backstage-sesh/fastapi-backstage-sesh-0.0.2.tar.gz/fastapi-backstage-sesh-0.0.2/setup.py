# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_backstage_sesh', 'fastapi_backstage_sesh.backends']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.68.1,<0.69.0',
 'itsdangerous>=2.0.1,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'starlette>=0.14.2,<0.15.0']

extras_require = \
{'examples': ['uvicorn[examples]>=0.15.0,<0.16.0']}

setup_kwargs = {
    'name': 'fastapi-backstage-sesh',
    'version': '0.0.2',
    'description': "FastAPI Middleware with simple Session implementation, plug n' playable",
    'long_description': "# FastAPI Backstage Sesh\n\n[![Build Status](https://app.travis-ci.com/aekasitt/fastapi-backstage-sesh.svg?branch=master)](https://travis-ci.com/aekasitt/fastapi-backstage-sesh)\n[![Package Vesion](https://img.shields.io/pypi/v/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)\n[![Format](https://img.shields.io/pypi/format/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)\n[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)\n[![License](https://img.shields.io/pypi/l/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)\n\n## Pluggable session support for FastAPI framework\n\nThis is an extension built on top of the strong foundation of `starsessions` by Alex Oleshkevich located here on [GitHub: alex-oleshkevich/starsessions](https://github.com/alex-oleshkevich/starsessions)\nYou can find the work on his Repo to be just as well compatible with your FastAPI App or other Starlette frameworks with ease. This repository will be a work extending on this strong foundation.\n\n## Roadmap\n\nI want to do two things with this project located here on this repository;\n\n1. Add an ease-of-use option for FastAPI's Background Task to share the same Session with User for long computational task.\n2. Add Redis Support as a `RedisBackend`\n\n## Installation\n\nInstall `fastapi-backstage-sesh` using PIP or poetry:\n\n```bash\npip install fastapi-backstage-sesh\n# or\npoetry add fastapi-backstage-sesh\n```\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n\n### Run Examples\n\nTo run the provided examples, first you must install extra dependencies [uvicorn](https://github.com/encode/uvicorn)\nRun the following command to do so\n\n```bash\npip install -U poetry\n# then\npoetry install --extras examples\n```\n\nAfter that you can start the example Apps using `Uvicorn`, a lightning-fast ASGI server implementation, with the following commands.\n\n```bash\nuvicorn examples.cookie:app\n# or\nuvicorn examples.memory:app\n```\n\nThese examples show you how to set up the basic configuration of the Middleware using Pydantic's `BaseModel` syntax and then adding to your FastAPI app using\n`app.add_middleware(BackstageSeshMiddleware)` snippet.\n\n## Contributions\n\nTo contribute to the project, fork the repository and clone to your local device and install preferred testing dependency [pytest](https://github.com/pytest-dev/pytest)\nAlternatively, run the following command on your terminal to do so:\n\n```bash\npoetry install\n```\n\nTesting can be done by the following command post-installation:\n\n```bash\npytest tests/*.py\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n",
    'author': 'Sitt Guruvanich',
    'author_email': 'aekasitt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/aekasitt/fastapi-backstage-sesh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
