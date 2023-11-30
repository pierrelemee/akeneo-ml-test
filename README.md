# akeneo-ml-test

Test ML Software Engineer @ Akeneo

[![unit-test](https://github.com/pierrelemee/akeneo-ml-test/actions/workflows/unit-test.yml/badge.svg)](https://github.com/pierrelemee/akeneo-ml-test/actions/workflows/unit-test.yml)

## Installation

This app is designed to work with Python 3.11+.

### Natively

If you prefer to run the app in an isolated environment, you can setup [`virtualenv`](https://virtualenv.pypa.io/en/latest/)
first:

```bash
python -m virtualenv venv
source venv/bin/activate
```

To get started, you'll have to install dependencies:

```bash
pip install -r requirements.txt
```

Then run the web server:
```bash
uvicorn web:app
```

You can now try it out from the [Swagger UI](http://127.0.0.1:8000/docs) or from the terminal using cURL:

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/api/product/fields/lookup' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "description": "Mon super produit qu''il est trop bien",
  "llm": "camellm",
  "fields": [
    "EF002169", "EF000010", "EF999999"
  ]
}'

```

### Using docker compose

Thanks to Docker compose you can start a container and 3rd parties dependencies really quickly.

```bash
# Create your own .env file based on the distributed example:
cp .env.dist .env
docker compose build
docker compose up -d
```

## Database preparation

Before requesting data, you have to ensure database is up-to-date and provisioned.

First, create tables by running migrations:

```bash
pw_migrate migrate --database $DATABASE_URL
```

Then you can provision the `fields` and `field_values` tables from the raw JSON files in the `data/` directory:

```bash
python ./cli.py
```

## Core concepts

Each product fields lookup query is made via a HTTP request to the dedicated endpoint (e.g. `POST /api/product/fields/lookup`).

Based on the selected LLM (either `llama2` or `camellm`), the corresponding implementation of the `AbstractLLM` will be
used to perform the query upon each one of the given fields. The two implementations of `AbstractLLM` in use
(see [the configuration section](#configuration)) have to created with customs `AbstractChainOfThoughts` and `AbstractConnector`.

Here is a quick recap of what is what:
* an `AbstractChainOfThoughts` takes as input a field, a product description (extra context from example ?) and builds a
query, e.g. `system_prompt` and `user_message`
* an `AbstractLLM` knows how to properly format the query for its model (and respect constraints like max length)
* an `AbstractConector` has the ability to talk to an actual LLM (command process, raw python, HTTP query)

## Configuration

The Product field lookup API is designed to be easily configurable. The core configuration must be declared in a
dedicated Python module file that will be imported ad startup. This module can be overriden with the `CONFIG_MODULE`
environment variable. By default, the [`config` module](config/example.py) is used.

Here's how should it looks like:

```py
def get_llama2():
    return MyLLaMA(MyLLaMAConnector(), MyChainOfThoughts())


async def get_camellm():
    return MyCameLLM(MyCameLLMConnector(), MyChainOfThoughts())
```

You can define environment variables either by _exporting_ them or at run:
```bash
CONFIG_MODULE=config.myconfig uvicorn web:app
```

You can find some _ready for use_ implementations of each type in `src.models.llms`, `src.models.chain_of_thoughts` and
`src.models.connectors` modules.

## Testing

Unit tests are performed using `pytest`. Dependencies for development and test environments are defined in the
`requirements-dev.txt` file. To run the test, you'll have to install these as well:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

Then you can simply run `pytest`:

```bash
pytest
```

## Design choices

I chose to use `FastAPI`, although I've never used this framework. In fact, when diving into the documentation I
realized it's far more than a web server library (like Flask) and there were 3 major concepts I could benefit in this
project:
* serialization via `pydantic` (embedded): quickly and easily transform object to JSON and inversely
* dependency injection: define external service classes and let the framework do the invocation and wiring. Here it also
brings the ability to do [_depenceny inversion_](https://en.wikipedia.org/wiki/Dependency_inversion_principle)
* ORM: connect to an external database simply while using simple domain objects

It took me some extra time to discover this new framework, but I'm glad to play with it and I wish I knew it before :)

Additionally, I chose to use the [Peewee ORM](http://docs.peewee-orm.com/en/latest/), for its strong inspiration of the Django ORM with the active record
approach. I used a PostgreSQL database and preferred to switch to Docker compose to ease the setup. And I rely on
[`peewee-migration`](https://github.com/klen/peewee_migrate).

And for the command-line utilities, I chose [`typer`](https://typer.tiangolo.com/) by the same author than FastAPI and
which offers great features.

Even if it seems obvious that queries to LLMs are mostly done via an HTTP query, I chose to use the _connector_ system.
This allows, among other benefits, to use plain Python code in a testing purpose. In a general consideration, I sense
there are many ways to "fine tune" the queries to both LLMs given the product / fields context. For this reason I
designed this _highly-configurable_ / _OOP based_ system that could be, at scale, redefined without deploy like it's
done with [feature flags](https://launchdarkly.com/blog/what-are-feature-flags/).

## Tasks

- [x] Set up the API endpoint and deserialize data
- [x] Write a first unit tests and automatize CI
- [x] Define model classes and plug a basic LLM query workflow
- [x] Make LLaMA& & CameLL logic configurable
- [x] Test LLaMA2 with Replicate
- [x] Prompt length management
- [x] Multi threading
- [x] Timeout management
- [x] Few shots in prompt using known examples (require ORM setup)


