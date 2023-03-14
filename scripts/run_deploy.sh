set -e

python manage.py wait-for-db
python manage.py create-db
python manage.py upgrade-db

gunicorn -b 0.0.0.0:8080 'osemu:create_app()' 
