# VoteSJSU - Backend

## Intro
This is the VoteSJSU backend that serves the Android and iOS clients.

The server is based on Python with Django and MySQL. Running and deployment is handled by docker-compose.

## Run the server
Ensure docker-compose is installed prior to running the server.
```
docker-compose build
docker-compose up
```
The server runs on port 8000. You can proceed to directly modify the source code in the `src` directory.

If you need to execute a command within docker, do the following:
```
# execute command
docker exec -ti <container-id> <command>
# for example, if I want a bash prompt in the django container
docker exec -ti VoteSJSU-django bash
# or to run test
docker exec -ti VoteSJSU-django ./manage.py test
# or to make migrations and migrate
docker exec -ti VoteSJSU-django ./manage.py makemigrations
docker exec -ti VoteSJSU-django ./manage.py migrate
```
