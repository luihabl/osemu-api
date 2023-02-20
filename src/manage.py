import os
import click
import subprocess
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

@click.group
def manage_cli():
    pass


def run_sql(statements):
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DEFAULT_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOSTNAME"),
        port=os.getenv("POSTGRES_PORT"),
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    for statement in statements:
        cursor.execute(statement)

    cursor.close()
    conn.close()


def postgres_test():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DEFAULT_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOSTNAME"),
            port=os.getenv("POSTGRES_PORT"),
        )

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
def test():
    run_sql([f"CREATE DATABASE {os.getenv('APP_DB')}"])
    subprocess.call(['pytest'])



@manage_cli.command(context_settings={"ignore_unknown_options": True})
def run():
    subprocess.call(['flask', 'run'])

if __name__ == "__main__":
    manage_cli()