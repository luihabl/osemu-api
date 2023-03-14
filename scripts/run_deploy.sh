set -e

python manage.py wait-for-db
python manage.py create-db
python manage.py upgrade-db
python manage.py create-default-admin-user

gunicorn -b 0.0.0.0:8000 'osemu:create_app()' 
