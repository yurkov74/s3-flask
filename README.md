# s3-flask
Example Flask app using self-hosted S3-alternative storage

Content:
- [About project](#about-project)
- [Setting up the project](#setting-up-the-project)
  - [Environment variables](#environment-variables)
- [Using the project](#using-the-project)


## About project

This project has been created with a purpose learning S3-compatible storage basics and using it within a small Flask app.
A single-node minIO server running on a docker image is using as an S3-alternative. More complecated storage configuration easily could be applied the same way.

The materials used during creating of this projects:
- [How to Upload Files from Flask to MinIO on Docker](https://medium.com/data-engineering-indonesia/how-to-upload-files-from-flask-to-minio-on-docker-14aade73596f)

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

## Using the project

The app is built on 2 services:
- minio: S3-compatible storage service for the files of the supported types (txt, pdf, png, jpg, jpeg, gif)
- web: a small web app service on python Flask library which allows us to learn and demonstrate some basic examples of working with S3 storage like uploading a file to the storage.

Both services are configured in the docker-compose.yml file and are running on the docker containers. The image for the web service is being built on the startup if it's hasn't been built yet or the code has been changed.

### Starting/stopping the app

```
docker compose up -d                # starting the S3 storage and the web app on docker images
docker compose down                 # stop the web app and the storage service
```

### Accessing the web app

The app's web service is available at localhost:5000

### S3-storage administration

The storage admin pannel should be available in the browser at localhost:9090