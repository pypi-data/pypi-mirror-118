# FastAPI Backstage Sesh

[![Build Status](https://app.travis-ci.com/aekasitt/fastapi-backstage-sesh.svg?branch=master)](https://travis-ci.com/aekasitt/fastapi-backstage-sesh)
[![Package Vesion](https://img.shields.io/pypi/v/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)
[![Format](https://img.shields.io/pypi/format/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)
[![Python Version](https://img.shields.io/pypi/pyversions/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)
[![License](https://img.shields.io/pypi/l/fastapi-backstage-sesh)](https://pypi.org/project/fastapi-backstage-sesh)

## Pluggable session support for FastAPI framework

This is an extension built on top of the strong foundation of `starsessions` by Alex Oleshkevich located here on [GitHub: alex-oleshkevich/starsessions](https://github.com/alex-oleshkevich/starsessions)
You can find the work on his Repo to be just as well compatible with your FastAPI App or other Starlette frameworks with ease. This repository will be a work extending on this strong foundation.

## Roadmap

I want to do two things with this project located here on this repository;

1. Add an ease-of-use option for FastAPI's Background Task to share the same Session with User for long computational task.
2. Add Redis Support as a `RedisBackend`

## Installation

Install `fastapi-backstage-sesh` using PIP or poetry:

```bash
pip install fastapi-backstage-sesh
# or
poetry add fastapi-backstage-sesh
```

## Quick start

See example application in `examples/` directory of this repository.

### Run Examples

To run the provided examples, first you must install extra dependencies [uvicorn](https://github.com/encode/uvicorn)
Run the following command to do so

```bash
pip install -U poetry
# then
poetry install --extras examples
```

After that you can start the example Apps using `Uvicorn`, a lightning-fast ASGI server implementation, with the following commands.

```bash
uvicorn examples.cookie:app
# or
uvicorn examples.memory:app
```

These examples show you how to set up the basic configuration of the Middleware using Pydantic's `BaseModel` syntax and then adding to your FastAPI app using
`app.add_middleware(BackstageSeshMiddleware)` snippet.

## Contributions

To contribute to the project, fork the repository and clone to your local device and install preferred testing dependency [pytest](https://github.com/pytest-dev/pytest)
Alternatively, run the following command on your terminal to do so:

```bash
poetry install
```

Testing can be done by the following command post-installation:

```bash
pytest tests/*.py
```

## License

This project is licensed under the terms of the MIT license.
