from flask import Flask, request
from flask_restful import Resource, Api
import base64
import getPixelRatio

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return {"home": 'Test '}
        
    def post(self):
        file_to_upload = request.files['file']
        imgR = cv2.imread(file_to_upload)
        wid = imgR.shape[1]
        hgt = imgR.shape[0]
        # print("Image Size {}x{}".format(wid,hgt))
        mask = getPixelRatio.tag_detection(imgR)
        img , corners ,length, pixelRatio = getPixelRatio.cameraCalibration(mask)
        # file = request.files.get('file')
        # json = request.get_json()
        json = "ss"
        return {'pixelRatio':pixelRatio}

class Multi(Resource):
    def get(self, num):
        return {'result':num*10}

api.add_resource(Test,'/')
api.add_resource(Multi,'/multi/<int:num>')

if __name__ == '__main__':
    app.run(debug=True)
