## Flask-SpaProxy

This extension expose either static resources using a reverse proxy in development, or
expose static resources using static folder from flask in production.

[![ci](https://github.com/FabienArcellier/Flask-SpaProxy/actions/workflows/ci.yml/badge.svg)](https://github.com/FabienArcellier/blueprint-library-pip/actions/workflows/ci.yml)

When developing an SPA with React, frontend resources are exposed
on an API endpoint. By default, this is exposed at `http: // localhost: 5100`.

In production, the behavior is different. Flask serves these resources as
static file.

This different operation makes the development of the Flask router
risky and complicates the alignment between the development environment and
that of production.

One of the symptoms of this problem is the addition of a CORS rule to address the fact
that the frontend is running on a different URL than the developing backend.

```python
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

`Flask-SpaProxy` allows with the same code to deal with this case.

If the variable `FLASK_SPA_PROXY_URL` exists, then Flask will call this endpoint to serve
the resources he does not know. If it is absent, Flask will serve the resources
from the `static_folder` folder.

### Don't use this extension when ...

The use of this extension is recommended only in the case where the frontend resources
are served by Flask.

If your Frontend is served by an nginx server or by a production CDN,
it is better to use the proxy provided by Webpack which will reproduce better
the final behavior of the application. Indeed, in this case, the Flask router is not
not solicited.

## Getting started

```bash
pip install Flask-SpaProxy
```

Write a simple flask application in `hello.py`

```python
from flask import Flask
from flask_spaproxy import SpaProxy

app = Flask(__name__)
SpaProxy(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

Before running the application

```bash
$ export FLASK_APP=hello
$ export FLASK_SPA_PROXY_URL=http://localhost:5001
$ flask run
```

## The latest version

You can find the latest version to ...

```bash
git clone https://github.com/FabienArcellier/Flask-SpaProxy.git
```

## Developper guideline

```
$ make
activate                       activate the virtualenv associate with this project
coverage                       output the code coverage in htmlcov/index.html
help                           provides cli help for this makefile (default)
install_requirements_dev       install pip requirements for development
install_requirements           install pip requirements based on requirements.txt
lint                           run pylint
tests                          run automatic tests
tests_units                    run only unit tests
update_requirements            update the project dependencies based on setup.py declaration
```

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
make install_requirements_dev
```

### Install production environment

```bash
make install_requirements
```

### Initiate or update the library requirements

If you want to initiate or update all the requirements `install_requires` declared in `setup.py`
and freeze a new `Pipfile.lock`, use this command

```bash
make update_requirements
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
make venv
source venv/bin/activate
```

### Use continuous integration process

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make ci
```

## Contributors

* Fabien Arcellier

## License

MIT License

Copyright (c) 2018 Fabien Arcellier

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
