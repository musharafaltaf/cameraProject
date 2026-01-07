import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import Flask, render_template, request
import base64
from datetime import datetime
import os

app = Flask(__name__)
cloudinary.config(
    cloud_name = "dqij85zsh",
    api_key = "428295586246342",
    api_secret = "qv9Dq6_18jJzjx40V7X1Ok2bMOg"
)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit


# Create static folder if not exists
if not os.path.exists("static"):
    os.mkdir("static")

@app.route("/")
def index():
    return render_template("camera.html")

@app.route("/save", methods=["POST"])
def save():
    data = request.form["image"]
    name = request.form["name"]

    image_data = data.split(",")[1]
    img = base64.b64decode(image_data)

    name = name.replace(" ", "_")

    filename = name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        img,
        public_id=filename
    )

    image_url = upload_result["secure_url"]

    # Show image using Cloudinary URL
    return render_template("result.html", name=name, image_url=image_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)


