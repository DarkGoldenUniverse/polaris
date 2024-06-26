# polaris
Polaris is commonly known as the North Star and has been used in navigation for centuries.

**Setup Virtual Environment**

```shell
python -m venv venv

source venv/bin/activate
```

**Install Packages**

```shell
pip install --upgrade django djangorestframework pre-commit

pip install -r requirements.txt
pre-commit install
```

**Add Package in Requirement file**

_if change in packages then update the requirements with below cmd_

```shell
pip freeze > requirements.txt
```

**Load the Environments for local development**

```shell
source env_vars.sh
```

**Migrate to your database**

```shell
python manage.py makemigrations

python manage.py migrate
```

**Create Super User**

```shell
python manage.py createsuperuser --username admin --email admin@example.com
```

**Runserver**

```shell
python manage.py runserver
```

**Seed Data**

_Dump data for specific models within an app_

```shell
python manage.py dumpdata inventory.category inventory.inventory customer.customer order.cart order.order > seed.json
```

_Load fixtures into the database_

```shell
python manage.py loaddata seed.json
```
