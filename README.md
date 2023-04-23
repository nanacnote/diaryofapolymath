## Diary of a Polymath

An extension of my mind

## Requirements

Node 16

Python 3.9

Pipenv 2021.5.29

### Setup

```
git clone https://github.com/nanacnote/diaryofapolymath.git
cd diaryofapolymath
cp .env.example .env
npm i
pipenv install --dev
chmod +x ./run
```

### Run

Preferred

```
./run start:dev
```

Manual

```
pipenv shell
export APP_ENV="development" # [development | production | test]
export PYTHONPATH="./src"
export DJANGO_SETTINGS_MODULE="base.settings.${APP_ENV}"
django-admin runserver
npm start
```
