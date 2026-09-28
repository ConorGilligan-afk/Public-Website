# Deploy notes

Droplet: crm-droplet (ssh alias)
Project path: /var/www/Public-Website
Virtualenv: /var/www/Public-Website/venv
Gunicorn service: gunicorn
Nginx site: /etc/nginx/sites-available/jrf

## Deploy
cd /var/www/Public-Website
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-jrf

## Logs
sudo journalctl -u gunicorn-jrf -n 50