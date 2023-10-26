from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from custom_utils import login, fetch_data, resolve_color_code
import io
import csv

ALLOWED_EXTENSIONS = {'csv'}
tmp_store = {}
app = Flask(__name__)
api = Api(app)

def allowed_file(filename)->bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_online_data():
    if "token" not in tmp_store:
        tmp_store["token"] = login()
    try:
        data = fetch_data(tmp_store['token'])
        return data
    except:
        tmp_store['token'] = login()
        return get_online_data()

def get_color_code(labelId: str):
    if "token" not in tmp_store:
        tmp_store['token'] = login()

    try:
        res = resolve_color_code(labelId, tmp_store['token'])
        return res
    except:
        tmp_store['token'] = login()
        return get_color_code()  

class MainApp(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({"error": "not file found"})
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'invalid file type, only csv files are accepted'})
        d = get_online_data()
        new_d = list(filter(lambda x: x['hu'], d))
        file_contents = file.read().decode('utf-8')
        uploaded_csv_file = io.StringIO(file_contents)
        csv_reader = csv.reader(uploaded_csv_file, delimiter=';')
        for row in csv_reader:
            print(row)
        return new_d

api.add_resource(MainApp, '/')

if __name__ == "__main__":
    app.run(debug=True)