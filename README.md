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

This should open the server at http://localhost:8000.

### Setup the mechanical survey

Open the admin page at http://localhost:8000/admin. Log in using the admin login details as created with the `createsuperuser` command before.

Now, open the following url http://localhost:8000/setup-mech-task. It will automatically create everything that is needed (like creating the treatment conditions, algorithms, read the students into the system etc.,)

## Testing different treatment arms

You can use the magic links to test any treatment arm as needed. To get the magic links, visit: http://localhost:8000/api/get-test-user/help.

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

Set the database you want to use in `survey/settings.py` file, and run migrations to set the schema. Access the DB like you normally would.

## App deployment

Follow the usual Django deployment methods.

### Set DEBUG = False

Open `survey/settings.py` file, change `DEBUG = True` to `DEBUG = False`. The file should look like follows:

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
3. Restart the gunicorn process (or a similar process)

Refer to the `./restart_server.sh` for an example script that you can use.


## Complex deployments - nginx changes

You need to really know what you're doing to make nginx changes. ALWAYS refer to the official docs, and test the config before restarting nginx.

Just run the following to restart nginx:

```bash
./restart_nginx.sh
```
