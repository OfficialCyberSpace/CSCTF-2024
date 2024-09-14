import logging
import os
import subprocess
import uuid

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
)

app = Flask(__name__)
upload_dir = "/tmp/"

app.config["MAX_CONTENT_LENGTH"] = 1 * 10**6  # 1 MB
app.config["SECRET_KEY"] = os.urandom(32)


@app.route("/", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("index.html")

    if "file" not in request.files:
        flash("No file part!", "danger")
        return render_template("index.html")

    file = request.files["file"]
    if file.filename.split(".")[-1].lower() != "zip":
        flash("Only zip files allowed are allowed!", "danger")
        return render_template("index.html")

    upload_uuid = str(uuid.uuid4())
    filename = f"{upload_dir}raw/{upload_uuid}.zip"
    file.save(filename)
    subprocess.call(["unzip", filename, "-d", f"{upload_dir}files/{upload_uuid}"])
    flash(
        f'Your file is at <a href="/files/{upload_uuid}">{upload_uuid}</a>!', "success"
    )
    logging.info(f"User uploaded file {upload_uuid}.")
    return redirect("/")


@app.route("/files/<path:path>")
def files(path):
    try:
        return send_from_directory(upload_dir + "files", path)
    except PermissionError:
        abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
