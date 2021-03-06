# For contributors

## Table of contents
* [HOWTO contribute]
* [Setting up virtual environment]
* [Installing requirements]
* [Running server live]
* [Running tests]
* [Running linter]


## HOWTO contribute
Preferred way is [Forking
Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
and using topic branches named after JIRA tickets


## Setting up virtual environment
Note: this part is OPTIONAL, but still recommended.

1. Create python3 virtualenv:
```
VENV_DIR="$HOME/.my_virtualenvs/wyin-be-feed"
mkdir -p "${VENV_DIR}"
python3 -m venv "${VENV_DIR}"
```
2. Switch to new virtualenv:
```
source "${VENV_DIR}/bin/activate"
```


## Installing requirements
```
make dev-install
```
or
```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```


## Running server live
```
make dev-run
```
or
```
uvicorn feed.main:app --reload
```


## Running tests
```
make test
```
or
```
pytest --disable-socket --cov=feed/ tests/
```


## Running linter
```
make lint
```
if you want to always run linter as pre-commit hook
```
pre-commit install
```



[HOWTO contribute]: #howto-contribute
[Setting up virtual environment]: #setting-up-virtual-environment
[Installing requirements]: #installing-requirements
[Running server live]: #running-server-live
[Running tests]: #running-tests
[Running linter]: #running-linter
