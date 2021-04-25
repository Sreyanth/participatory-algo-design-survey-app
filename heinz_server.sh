# Regular manual server
# sudo ../venv/bin/python3 manage.py runserver 0.0.0.0:80

# Run the server using gunicorn
sudo ../venv/bin/gunicorn -b 0.0.0.0:80 --env DJANGO_SETTINGS_MODULE=survey.settings -D survey.wsgi

# Restart the server gracefully
# kill -HUP `ps -C gunicorn fch -o pid | head -n 1`
