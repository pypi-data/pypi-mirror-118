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
    'version': '0.0.1',
    'description': "FastAPI Middleware with simple Session implementation, plug n' playable",
    'long_description': "# FastAPI Backstage Sesh\n\n## Pluggable session support for FastAPI framework\n\nThis is an extension built on top of the strong foundation of `starsession` by Alex Oleshkevich located here on [GitHub: alex-oleshkevich/starsessions](https://github.com/alex-oleshkevich/starsessions)\nYou can find the work on his Repo to be just as well compatible with your FastAPI App or other Starlette frameworks with ease. This repository will be a work extending on this strong foundation.\n\n## Roadmap\n\nI want to do two things with this project located here on this repository;\n\n1. Add an ease-of-use option for FastAPI's Background Task to share the same Session with User for long computational task.\n2. Add Redis Support as a `RedisBackend`\n\n## Installation\n\nInstall `fastapi-backstage-sesh` using PIP or poetry:\n\n```bash\npip install fastapi-backstage-sesh\n# or\npoetry add fastapi-backstage-sesh\n```\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n\n### Run Examples\n\nTo run the provided examples, first you must install extra dependencies [uvicorn](https://github.com/encode/uvicorn)\nRun the following command to do so\n\n```bash\npip install -e .[examples]\n# or\npoetry install --extras examples\n```\n",
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
