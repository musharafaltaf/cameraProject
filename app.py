from flask import Flask, render_template, request
import base64
from datetime import datetime
import os

app = Flask(__name__)
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

    filename = name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join("static", filename)

    with open(filepath, "wb") as f:
        f.write(img)

    # Send filename to result page
    return render_template("result.html", name=name, filename=filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

