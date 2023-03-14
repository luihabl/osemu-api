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
            exit(1)

    print('Database available!')
    exit(0)

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
def fetch_github_data():
    
    from osemu import create_app
    from osemu.extensions import db
    from osemu.api.views.base_views import get_or_create_obj
    from osemu.api import schema
    from github import Github
    from datetime import datetime
    
    app = create_app()
    app.app_context().push()
    db.create_all()

    token = os.environ.get('GITHUB_TOKEN', None)
    if token:
        gh = Github(os.getenv('GITHUB_TOKEN'))
    else:
        print('No APIToken available.')
        exit(1)

    emulators : list[Emulator] = db.session.query(Emulator).all()
    for emu in emulators:
        gh_url = emu.git_url
        
        if not gh_url or gh_url == '':
            print(f'No git url defined.')
            continue

        print(f'Updating data of {emu.name} @ {gh_url}')

        if gh_url.endswith('/'):
            gh_url = gh_url.rstrip('/')
            emu.git_url = gh_url
        
        id = '/'.join(gh_url.split('/')[-2:])
        repo = gh.get_repo(id)

        emu.gh_stars = repo.stargazers_count
        emu.gh_forks = repo.forks_count

        latest_commit = repo.get_commits()[0]
        emu.latest_update = datetime.strptime(latest_commit.last_modified, '%a, %d %b %Y %H:%M:%S %Z')
        emu.release_date = repo.created_at

        languages = []
        langs = repo.get_languages()
        for lang_name, lang_amount in langs.items():

            lang_obj = db.session.query(Language).filter_by(name=lang_name).first()
            if not lang_obj:
                lang_obj = Language(name=lang_name)
                emu_lang = EmulatorLanguage(language=lang_obj, emulator=emu, amount=lang_amount)
            else:
                emu_lang = db.session.query(EmulatorLanguage).filter_by(language=lang_obj, emulator=emu).first()
                if not emu_lang:
                    emu_lang = EmulatorLanguage(language=lang_obj, emulator=emu, amount=lang_amount)
                else:
                    emu_lang.amount = lang_amount

            languages.append(emu_lang)

        emu.language_amounts = languages

        license = None
        try:
            license = repo.get_license()
        except:
            print(f'No license found for {emu.name}')
            emu.license = None
        
        if license:
            name = license.license.name

            try:
                url = license.license.html_url
            except:
                url = ''

            if name == 'Other':
                name = f'{emu.name} License'
                url = license.html_url

            lic_obj = db.session.query(License).filter_by(name=name).first()

            if not lic_obj:
                lic_obj = License(name=name, url=url)
            
            lic_obj.url = url
            
            emu.license = lic_obj

        emu.short_description = repo.description

        if repo.homepage:
            emu.website_url = repo.homepage

    try:
        db.session.commit()
    except:
        db.session.rollback()

 

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


@manage_cli.command(context_settings={"ignore_unknown_options": True})
def create_default_admin_user():
    from osemu import create_app
    from osemu.extensions import db

    app = create_app()
    app.app_context().push()
    db.create_all()

    #crate user
    from osemu.api.views.auth import check_and_register_user
    from marshmallow import ValidationError

    email = os.environ.get('ADMIN_USER_EMAIL', None)
    password = os.environ.get('ADMIN_USER_PASSWORD', None)

    if email is None or password is None:
        print('No admin info provided.')
        exit(1)

    try:
        check_and_register_user({'email': email, 'password': password})    
    except (ValidationError, ValueError) as err:
        print(err)
        exit(1)



if __name__ == "__main__":
    manage_cli()