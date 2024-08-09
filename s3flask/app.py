from flask import Flask, request, redirect, render_template, url_for
from werkzeug.utils import secure_filename
from minio import Minio
import os

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")


client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)


def upload_object(client, filename, data, length):

    # Make bucket if not exist.
    found = client.bucket_exists(BUCKET_NAME)
    if not found:
        client.make_bucket(BUCKET_NAME)
    else:
        print(f"Bucket {BUCKET_NAME} already exists")

    client.put_object(BUCKET_NAME, filename, data, length)
    print(f"{filename} is successfully uploaded to bucket {BUCKET_NAME}.")


def allowed_file(filename):
    return "." in filename and filename.rsplit(
            ".", 1
        )[1].lower() in ALLOWED_EXTENSIONS


def get_download_link(obj_name):
    return client.get_presigned_url(
        'GET',
        BUCKET_NAME,
        obj_name
    )


app = Flask(__name__, template_folder='./templates')
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            size = os.fstat(file.fileno()).st_size
            upload_object(client, filename, file, size)
            return redirect(request.url)

    # get a bucket's file list
    objects = []
    if client.bucket_exists(BUCKET_NAME):
        storage_objects = client.list_objects(BUCKET_NAME)
        for so in storage_objects:
            objects.append((so, get_download_link(so.object_name)))

    return render_template('home.html', objects=objects)


@app.route("/<obj_name>/delete")
def delete_object(obj_name):
    client.remove_object(BUCKET_NAME, obj_name)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
