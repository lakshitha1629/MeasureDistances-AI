from flask import Flask, request, redirect, jsonify
import os
import json
import re
import base64
from func import cameraCalibration

app = Flask(__name__)

UPLOAD_FOLDER = 'received_files'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def print_request(request):
    # Print request url
    print(request.url)
    # print relative headers
    print('content-type: "%s"' % request.headers.get('content-type'))
    print('content-length: %s' % request.headers.get('content-length'))
    # print body content
    if request.is_json:
        json_data = request.get_json(cache=True)
        # replace image_data with '<image base64 data>'
        if json_data.get('image_data', None) is not None:
            json_data['image_data'] = '<image base64 data>'
        else: 
            print('request image_data is None.')
        print(json.dumps(json_data,indent=4))
    else: # form data
        body_data=request.get_data()
        # replace image raw data with string '<image raw data>'
        body_sub_image_data=re.sub(b'(\r\n\r\n)(.*?)(\r\n--)',br'\1<image raw data>\3', body_data,flags=re.DOTALL)
        print(body_sub_image_data.decode('utf-8'))
    # print(body_data[0:500] + b'...' + body_data[-500:]) # raw binary

@app.route('/', methods=['GET','POST'])
def index():
    if(request.method == 'POST'):
        # JSON data format
        if request.is_json:
            """ Sample data
            {'file_format':'jpg', 'image_data': <base64 ascii string>}
            """
            # print('Request is a JSON format.')
            json_data = request.get_json(cache=False)
            file_format = json_data.get('file_format', None)
            image_data = json_data.get('image_data', None)
            if file_format not in ALLOWED_EXTENSIONS or image_data is None:
                return '{"error":"Invalid JSON."}'

            file = os.path.join(UPLOAD_FOLDER, 'image.' + file_format)
            with open(file,'wb') as f:
                # Note: Convert ascii string to binary string first, e.g. 'abc' to b'abc', before decode as base64 string.
                f.write(base64.b64decode(image_data.encode('ascii'))) 
        
        # form data format
        else: 
            # check if the post request has the file part
            if 'file' not in request.files:
                print('No file part')
                return redirect(request.url)
            file = request.files.get('file')
            # if user does not select file, browser also submit an empty part without filename
            if file.filename == '':
                print('No selected file')
                return redirect(request.url)

            if not allowed_file(file.filename):
                return '{"error":"Invalid image file format."}'

        name = 'ss'
        # name = 
        pixelRatio = cameraCalibration(file)
        return jsonify({'you sent':name})

    else:
        return jsonify({"about":'Hello, World!'})

if __name__=='__main__':
    app.run(debug=True)