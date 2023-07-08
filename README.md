## Diary of a Polymath

An extension of my mind

## Requirements

Node 16

Python 3.9

Pipenv 2021.5.29

Docker

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
export APP_ENV=development          # development | production | test
export PYTHONPATH="./src"
export DJANGO_SETTINGS_MODULE="base.settings.${APP_ENV}"
django-admin runserver
npm start
```

#### Preferred

```bash
./run start:dev                     # starts both django and vite servers
./run start:django:debugger         # starts only the django server in pdb mode
```

### Linting

```bash
./run start:lint
./run start:lint:fix
```

### Test

```bash
./run start:test                    # extra arguments will be passed to pytest
```

### SCM Strategy

#### Main branch

> 1. The production site is deployed from this branch.
> 1. Only the staging branch can be merged into the main branch.

#### Hotfix branch

> 1. No deployment from this branch.
> 1. Hotfix branch must always be kept up to date with staging before branching from it.
> 1. Branch from hotfix to start implementing a fix for a bug reported on the staging branch.
> 1. After implementing the bug fix, commit it to the hotfix branch, then merge the hotfix branch back into staging.

#### Staging branch

> 1. The staging site is deployed from this branch.
> 1. Only the hotfix branch and the develop branch can be merged into the staging branch.

#### Develop branch

> 1. No deployment from this branch.
> 1. Branch from develop to start implementing a new feature.
> 1. After fully implementing the feature, commit it back to the develop branch.
