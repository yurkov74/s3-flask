from flask import Flask, request, redirect
from werkzeug.utils import secure_filename
from minio import Minio
import os

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
ACCESS_KEY = os.environ.get("MINIO_ROOT_USER")
SECRET_KEY = os.environ.get("MINIO_ROOT_PASSWORD")
BUCKET_NAME = os.environ.get("MINIO_BUCKET")
MINIO_API_HOST = os.environ.get("MINIO_ENDPOINT")


def upload_object(filename, data, length):
    client = Minio(MINIO_API_HOST, ACCESS_KEY, SECRET_KEY, secure=False)

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


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def upload_file():
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
            upload_object(filename, file, size)
            return redirect(request.url)

    html_doc = """
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta
                    name="viewport"
                    content="width=device-width, initial-scale=1.0">
                <title>UPLOAD</title>
            </head>
            <body>
                <h1>Upload File</h1>
                <form method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                    <hr>
                </form>
            </body>
        </html>
        """
    return html_doc


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
