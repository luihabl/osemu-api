set -e

echo "--- Waiting for database ---"
python manage.py wait-for-db

echo "--- Creating database ---"
python manage.py create-db

echo "--- Upgrading database ---"
python manage.py upgrade-db

echo "--- Creating default user ---"
python manage.py create-default-admin-user

echo "--- Starting app ---"
gunicorn -b 0.0.0.0:8000 'osemu:create_app()' 
