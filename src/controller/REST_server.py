from flask import Flask, request, jsonify
from PIL import Image

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    num1 = int(request.json['num1'])
    num2 = int(request.json['num2'])

    return f'The sum of {num1} and {num2} is {num1 + num2}'


@app.route('/equation', methods=['POST'])
def predict():
    format_type = request.args.get('format_type', default=None)

    if format_type in ['file', 'url']:
        if format_type == 'file':
            try:
                image = Image.open(io.BytesIO(request.files["img1"].read()))
                return jsonify({'message': 'Success!'})
            except:
                ret = create_response({}, '3', 'Incorrect image format')
                return ret


if __name__ == '__main__':
    app.run(debug=True)