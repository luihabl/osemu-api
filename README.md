# Open source emulator database API

This is a small (WIP) personal project for creating a REST API for a database of open source emulator projects hosted on GitHub. The API was built using [Flask](https://flask.palletsprojects.com) and data persistence is done with PostgreSQL/[SQLAlchemy](https://www.sqlalchemy.org). The project uses docker containers for development and deployment. 

## Overview

The API endpoints are divided in seven groups:

- `/api/auth`: user authentication.
- `/api/consoles`: information about consoles.
- `/api/emulators`: information about emulators.
- `/api/companies`: information about companies (that make consoles).
- `/api/languages`: information about programming languages.
- `/api/licenses`: information about licenses. 

For more complete documentation of the available endpoints and methods, the API uses OpenAPI 3 with Swagger UI for documentation. The documentation page can be accessed through:

- `/api/docs`

The generation of the specs is done using [apispec](https://github.com/marshmallow-code/apispec) and the Swagger UI is generated with [flask-swagger-ui](https://github.com/sveint/flask-swagger-ui). 

The API has an admin panel created with [Flask-Admin](https://github.com/flask-admin/flask-admin), and it can be accessed in:

- `/admin`

The API uses session cookies for authentication with [Flask-Login](https://github.com/maxcountryman/flask-login). In the API only GET requests are allowed for unauthenticated users. 

User creation can only be done by authenticated users sending a POST request to `/auth/user`. Therefore, you need to create an initial admin user, which can be done with the manage command `python manage.py create-admin-user <example@example.com>`. However, every time you run the app it will run the command `create-default-admin-user`, which will create a user with the credentials given in the environment variables `ADMIN_USER_EMAIL` and `ADMIN_USER_PASSWORD`. So you can use these credentials to login initially. 

The project uses [APScheduler](https://github.com/agronholm/apscheduler) for scheduling a task for updating the emulator entries on a daily basis using the GitHub REST API. 


## Development

To run the project for development you can clone it and run it through docker compose, with 

```sh
docker compose up
```

The `src/` folder is mapped to the folder inside the container, so you can modify the code without the need to restart it. When the `up` command is executed, another container with the database is created and connected to the app. 

## Testing 

The tests in the project are performed using [pytest](https://docs.pytest.org/), and are placed in `src/osemu/tests`.

There is a dedicated docker compose file (`docker-compose-test.yml`) and a shell script (`scripts/run_tests_docker.sh`) for the tests. To run them you can execute the script by `sh ./scripts/run_tests_docker.sh` from the project directory. This script is also used by GitHub actions to perform the tests at every commit.

A dedicated database is created for the tests, so they can be executed at the same time the development server is running without risks of losing data. 

## Deployment

The flask app is deployed with a dedicated Dockerfile (`Dockerfile.deploy`) without docker compose. This is done so that the app can be deployed as a single container with the database being hosted separately.

For the deployment it is necessary to provide all the required environment variables, which are typically provided in the docker compose file. Furthermore, it is required that you provide the variable `GITHUB_TOKEN` with a token for the GitHub API, if you want the app to retrieve automatically data from GitHub. 

The API is currently being hosted on Fly.io, and `fly.toml` is the configuration for the deployment process of the platform.  

## Front-end

The OSEmu API has a front-end created with NextJS. Its code is hosted in the repository [luihabl/osemu-frontend](https://github.com/luihabl/osemu-frontend).