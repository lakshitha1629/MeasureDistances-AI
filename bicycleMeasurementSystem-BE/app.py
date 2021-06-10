from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS
import base64
from func import cameraCalibration
import os
import re

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
UPLOAD_FOLDER = './upload'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Main(Resource):
    def get(self):
        return 'Welcome to, Bicycle Measurement System API!'
    
    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'post': value}, 201
            
            return {"error":"Invalid format."}
            
        except Exception as error:
            return {'error': error}

class GetRatio(Resource):
    def get(self):
        return {"error":"Invalid Method."}

    def post(self):
        file_to_upload = request.files['file']

        if file_to_upload.filename == '':
            print('No selected file')
            return redirect(request.url)

        if not allowed_file(file_to_upload.filename):
            return {"error":"Invalid image file format."}

        try:
            path = os.path.join(app.config['UPLOAD_FOLDER'], file_to_upload.filename)
            file_to_upload.save(path)
            pixelRatio = cameraCalibration(path)
            return {'pixelRatio':pixelRatio}

        except Exception as error:
            return {'error': error}


api.add_resource(Main,'/')
api.add_resource(GetRatio,'/getRatio')

if __name__ == '__main__':
    app.run(debug=True)
