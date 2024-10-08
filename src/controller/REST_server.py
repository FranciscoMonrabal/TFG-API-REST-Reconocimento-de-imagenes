from flask import Flask, request, send_file
from PIL import Image
import io
import sys

sys.path.insert(0, r"C:\Users\paak1\Documents\PythonRepos\TFG\TFG-API-REST-Reconocimento-de-imagenes\src")

from config import Config
from model.inference import run_interference

app = Flask(__name__)


@app.route('/equation', methods=['POST'])
def predict():

    format_type = request.args.get('format_type', default=None)

    if format_type in ['file', 'url']:
        if format_type == 'file':
            try:
                config = Config()
                image = Image.open(io.BytesIO(request.files["img1"].read()))
                image.save(config.get_image_path(), "JPEG")
            except:
                return "Inappropriate format file", 400

            result, send_image_path = run_interference(config)
            return send_file(send_image_path)


if __name__ == '__main__':
    app.run(debug=True, host="26.203.10.79")

