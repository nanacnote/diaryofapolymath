## Diary of a Polymath

An extension of my mind

## Requirements

Node 16

Python 3.9

Pipenv 2021.5.29

Docker

> At least **2GB** of memory, especially for docker image build container (pyscopg is built from source and has this requirement). See [docker memory docs](https://docs.docker.com/config/containers/resource_constraints).

### Setup

```bash
git clone https://github.com/nanacnote/diaryofapolymath.git
cd diaryofapolymath
chmod +x ./run
cp .env.example .env
npm i
pipenv install --dev
pipenv shell
pre-commit install
```

### Run

#### Manual

```bash
pipenv shell
export APP_ENV=development          # [development] [production] [test]
export PYTHONPATH="./src:${PYTHONPATH}"
export DJANGO_SETTINGS_MODULE="base.settings.${APP_ENV}"
django-admin runserver
npm start
```

#### Preferred

```bash
./run start:dev                     # Start both Django and Vite servers.
./run start:django:debugger         # Start the Django server in pdb (debugger) mode.
```

### Linting

```bash
./run start:lint                    # Scan the codebase and report any linting issues.
./run start:lint:fix                # Scan the codebase and automatically fix any linting issues.
```

### Test

```bash
./run start:test                    # Run tests using pytest. Additional arguments can be passed.
```

### Release

```bash
./run start:release                    # In CI, tag the main branch with a release version number and include a change log.
```

### Commit Strategy

Pre-commit hooks are in place to enforce consistent commit messages.

[Hook](https://github.com/commitizen-tools/commitizen)

[Specification](https://www.conventionalcommits.org/en/v1.0.0/)

### SCM Strategy

#### Main branch

> 1. The production site is deployed from this branch.
> 1. Only the staging branch can be merged into the main branch.

#### Hotfix branch

> 1. No deployment from this branch.
> 1. Hotfix branch must always be kept up to date with staging before branching from it.
> 1. Branch from hotfix to start implementing a fix for a bug reported on the staging branch.
> 1. After implementing the bug fix, open a PR to the hotfix branch.

#### Staging branch

> 1. The staging site is deployed from this branch.
> 1. Only the hotfix branch and the develop branch can be merged into the staging branch.

#### Develop branch

> 1. No deployment from this branch.
> 1. Branch from develop to start implementing a new feature.
> 1. After fully implementing the feature, open a PR to the develop branch.
