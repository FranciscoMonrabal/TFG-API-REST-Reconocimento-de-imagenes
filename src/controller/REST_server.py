from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import uuid
from os import path

app = Flask(__name__)


@app.route('/equation', methods=['POST'])
def predict():

    images_path = "../../images/"
    format_type = request.args.get('format_type', default=None)

    if format_type in ['file', 'url']:
        if format_type == 'file':
            try:
                image = Image.open(io.BytesIO(request.files["img1"].read()))
                filename = str(uuid.uuid4())
                img_path = path.join(images_path, "recieved_imgs", f"{filename}.jpeg")
                image.save(img_path, "JPEG")

                # call the inference and return the image
                return jsonify({'message': 'Success!'})
            except:
                ret = create_response({}, '3', 'Incorrect image format')
                return ret


if __name__ == '__main__':
    app.run(debug=True)

