# Activate venv
source ../venv/bin/activate

# Make migrations and migrate the DB
./manage.py makemigrations
./manage.py migrate

# Collect the static files
./manage.py collectstatic

# Restart the gunicorn server
sudo systemctl restart gunicorn

# Deactivate venv
deactivate
