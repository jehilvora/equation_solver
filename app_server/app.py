from flask import Flask, request
from PIL import Image
from io import BytesIO
import base64
import time
from ocr import equation_ocr

app = Flask(__name__)

STATIC_PATH = "/Users/i506655/Projects/equation_solver/app_server/static"

@app.route("/processImage", methods=['POST'])
def processImage():
    imageData = request.get_json()
    if imageData["image"] != None:
        im = Image.open(BytesIO(base64.b64decode(imageData['image'])))
        imagePath = STATIC_PATH + "/{}.jpg".format(str(time.time()))
        im.save(imagePath)
        stringRes = equation_ocr.convertImageToText(imagePath)
        print(stringRes)
        return stringRes
    else:
        return "Error"

@app.route("/ping")
def ping():
    return "ping"

if __name__ == "__main__":
    app.run(debug=True)