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
