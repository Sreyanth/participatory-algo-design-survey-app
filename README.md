# Participatory Algorithm Design - Survey App

## Dev setup

### Environment setup

If you are developing / working on this app, you will need a virtual environment with Python 3.8 (NOT 3.9 as numpy installation isn't updated for Py3.9 yet).

Install all the required packages as mentioned in the requirements.txt file.

```bash
pip install -r requirements.txt
```

### One-time setup

Create the DB and tables.

```bash
# create the DB tables
./manage.py makemigrations
./manage.py migrate

# create admin user
./manage.py createsuperuser
```

### Start the server

```
./run_dev_server.sh
```

This should open the server at [localhost:8000](localhost:8000).

### Setup the mechanical survey

Open the admin page at [localhost:8000/admin](localhost:8000/admin). Log in using the admin login details as created with the `createsuperuser` command before.

Now, open the following url [localhost:8000/setup-mech-task](localhost:8000/setup-mech-task). It will automatically create everything that is needed (like creating the treatment conditions, algorithms, read the students into the system etc.,)

## Testing different treatment arms

You can use the magic links to test any treatment arm as needed. To get the magic links, visit: [localhost:8000/api/get-test-user/help](localhost:8000/api/get-test-user/help).

Visiting any of these links will automatically create a dummy user and assign that user to that specific treatment arm (instead of the randomization).

## Codebase structure

The entire code base is structured as follows:

```bash
api                   # API-related views
mech_task_setup       # views for setting up the survey for the first time
survey                # project folder with settings and URLs and so on
webapp                # entire mech task views, templates, URLs etc.,
```

## Accessing the data

### In development

We use SQLite as the database in the dev environment. The file `db.sqlite3` is where all the data is stored.

### In production

We use PostgreSQL as the database in production. You can use the `psql` tool to access the tables and exporting the data into CSV. Right now, there is no backup script for this.

You can't access the data with any PGAdmin tool as the port 5432 is not publicly accessible.

## App refresh / deployment

> **NOTE:** Always deploy the `main` branch. If there is a different branch, that branch MUST be pulled into the `main` branch after appropriate testing.

### Get the new codebase

Use `git` to get the new codebase in the `main` branch.

```bash
# Stash the current changes - if any
sudo git stash

# Get the new code
sudo git pull
```

### Set DEBUG = False

Open `survey/settings.py` file, change `DEBUG = True` to `DEBUG = False` (line 17). The file should look like follows:

```python
# ...

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ...
```

### Deploy

Whenever the site is updated (backend or frontend), we will have to deploy the website again. The way we implemented it, we just need to follow these steps:

1. If there is a DB change, make migrations, and apply them
2. If there are any static file changes, collect the static files to put in the `static` folder automatically
3. Need to restart the gunicorn process

Just run the following command that takes care of all of the above steps:

```bash
./restart_server.sh
```

## Complex deployments - nginx changes

You need to really know what you're doing to make nginx changes. ALWAYS refer to the official docs, and test the config before restarting nginx.

Just run the following to restart nginx:

```bash
./restart_nginx.sh
```
