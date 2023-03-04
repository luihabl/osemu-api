import os
import click
import subprocess
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from osemu.api.models import *

@click.group
def manage_cli():
    pass

def call_and_exit(cmd):
    exit(subprocess.call(cmd))

def connect_db():
    """Connect to DB and get connection object."""
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DEFAULT_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def run_sql(cursor, statements):
    for s in statements:
        cursor.execute(s)

def postgres_test():
    try:
        conn = connect_db()
        conn.close()
        return True
    except Exception as err:
        print(err)
        return False

@manage_cli.command(context_settings={"ignore_unknown_options": True})
def wait_for_db():
    total = 0
    while not postgres_test():
        print('Database not available...')
        time.sleep(1)
        total += 1
        if total > 10:
            print('Giving up.')
            return 1

    print('Database available!')
    return 0

@manage_cli.command(context_settings={"ignore_unknown_options": True})
def create_db():

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{os.getenv('APP_DB')}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {os.getenv('APP_DB')}")

    cursor.close()
    conn.close()


@manage_cli.command(context_settings={"ignore_unknown_options": True})
def upgrade_db():

    from osemu import create_app
    from osemu.extensions import db
    from flask_migrate import upgrade, migrate, stamp

    app = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    stamp()
    migrate()
    upgrade()

@manage_cli.command(context_settings={"ignore_unknown_options": True})
def test():
    call_and_exit('pytest')

@manage_cli.command(context_settings={"ignore_unknown_options": True})
def run():

    # Load env
    call_and_exit(['flask', 'run'])


@manage_cli.command(context_settings={"ignore_unknown_options": True})
@click.argument('email', type=click.STRING)
def create_admin_user(email):

    from osemu import create_app
    from osemu.extensions import db
    from flask_migrate import upgrade, migrate, stamp

    app = create_app()
    app.app_context().push()
    db.create_all()

    import getpass
    password1 = getpass.getpass('Enter a password:')
    password2 = getpass.getpass('Enter the same password:')

    if password1 != password2:
        print('Passwords do not coincide.')
        exit(1)
    
    if password1 == '':
        print('Password cannot be empty.')
        exit(1)
    
    #crate user
    from osemu.api.views.auth import check_and_register_user
    from marshmallow import ValidationError
 
    try:
        check_and_register_user({'email': email, 'password': password1})    
    except (ValidationError, ValueError) as err:
        print(err)
        exit(1)

if __name__ == "__main__":
    manage_cli()