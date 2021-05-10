# All commands are from: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

# Check for issues and restart Nginx
sudo nginx -t && sudo systemctl restart nginx

# If the gunicorn daemon is changed, copy the following commands manually
# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn
