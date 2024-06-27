# Polaris

Polaris is commonly known as the North Star and has been used in navigation for centuries.

---

## Local Development Command

```shell
source venv/bin/activate && source .env
docker-compose -f backend.yaml up -d

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com
python manage.py loaddata seed.json

python manage.py runserver 0.0.0.0:8000
```

---

## Setup

### 1. Setup Virtual Environment

```shell
python -m venv venv

source venv/bin/activate
```

### 2. Install Packages

```shell
pip install --upgrade django djangorestframework django-redis hiredis django-cors-headers pre-commit drf-spectacular
```

`OR`

```shell
pip install -r requirements.txt
```

### 3. Add Package in Requirement file and configure pre-commit

_if change in packages then update the requirements with below cmd_

```shell
pip freeze > requirements.txt

pre-commit install
```

---

## Configure Django Project

### 1. Load the Environments for local development

```shell
cp ./.env.template ./.env

source .env
docker-compose -f backend.yaml up -d
```

### 2. Migrate to your database

```shell
python manage.py makemigrations

python manage.py migrate
```

### 3. Create Super User

```shell
python manage.py createsuperuser --username admin --email admin@example.com
```

### 4. Runserver

```shell
python manage.py runserver 0.0.0.0:8000
```

---

## Seed Data

### 1. Dump Seed Data into file

_Dump data for specific models within an app_

```shell
python manage.py dumpdata inventory.category inventory.store inventory.inventory > seed.json
```

### 2. Load Seed Data from file

_Load fixtures into the database_

```shell
python manage.py loaddata seed.json
```

---
