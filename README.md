# s3-flask
Example Flask app using self-hosted S3-alternative storage

Content:
- [About project](#about-project)
- [Setting up the project](#setting-up-the-project)
  - [Environment variables](#environment-variables)
  - [hosts](#hosts)
- [Using the project](#using-the-project)
  - [Basic info](#basic-info)
  - [Starting/stopping the app](#startingstopping-the-app)
  - [Accessing the web app](#accessing-the-web-app)
  - [S3-storage administration](#s3-storage-administration)


## About project

This project has been created with a purpose learning S3-compatible storage basics and using it within a small Flask app.
A single-node minIO server running on a docker image is using as an S3-alternative. More complecated storage configuration easily could be applied the same way.

The materials used during creating of this projects:
- [How to Upload Files from Flask to MinIO on Docker](https://medium.com/data-engineering-indonesia/how-to-upload-files-from-flask-to-minio-on-docker-14aade73596f)
- [MinIO for developers - official mini-tutorial](https://youtube.com/playlist?list=PLFOIsHSSYIK37B3VtACkNksUw8_puUuAC&si=xsmtzyfDA3Q5cKMU)

The project's web part has been written and tested on Python v3.12.4.

## Setting up the project

### Environment variables

Please create .env file in the root of the project with the following entries (modify values accordingly to your configuration as you wish):
```
SECRET_KEY=secret-key
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=noprodpasswd
MINIO_VOLUMES="/data"
MINIO_SERVER_PORT=9000
MINIO_HOST=minio
MINIO_BUCKET=flask
MINIO_ENDPOINT=${MINIO_HOST}:${MINIO_SERVER_PORT}
```

### hosts

In order to make the download feature working properly please add our storage host domain name (which we have defined as MINIO_HOST environment variable in .env file, by default it's 'minio') to the hosts file on your local machine.
```
127.0.0.1			minio
```

## Configure the project lically

### Virtual environment

```
cd <project-root-folder>                      # go to the project's folder
# linux
python3 -m pip install --upgrade pip          # upgrade global pip
python3 -m venv venv                          # install virtual environment
source venv/bin/activate                      # activate virtual environment
(venv) python3 -m pip install --upgrade pip   # upgrade pip in the venv
# windows
pip install --upgrade pip                     # upgrade global pip
python -m venv venv                           # install virtual environment
venv/scripts/activate                             # activate virtual environment
(venv) python -m pip install --upgrade pip    # upgrade pip in the venv
```

Deactivate virtual environment:
```
(venv) deactivate
```

### Project dependencies

```
cd <project-root-folder>/src                  # go to the source code rrot folder
(venv) pip install -r requirements.txt        # app dependencies
```

## Using the project

### Basic info

The app is built on 2 services:
- minio: S3-compatible storage service for the files of the supported types (txt, pdf, png, jpg, jpeg, gif)
- web: a small web app service on python Flask library which allows us to learn and demonstrate some basic examples of working with S3 storage like uploading a file to the storage, downloading or deleting it.

Both services are configured in the docker-compose.yml file and are running on the docker containers. The image for the web service is being built on the startup if it's hasn't been built yet or the code has been changed.

### Starting the web service locally

Comment web service in the docker-compose.yml for that.
```
cd <project-root-folder>                      # go to the project's folder
(venv) flask --app s3flask/app run            # start the flask app in normal mode
(venv) flask --app s3flask/app run --debug    # start the flask app in debug mode
```

### Starting/stopping the app

```
docker compose up -d                # starting the S3 storage and the web app on docker images
docker compose down                 # stop the web app and the storage service
```

### Accessing the web app

The app's web service is available at http://localhost:5000

### S3-storage administration

The storage admin pannel should be available in the browser at http://localhost:9090