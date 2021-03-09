import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import flash

from keras.models import Sequential, load_model
import keras,sys
import numpy as np
from PIL import Image

classes = ["pants","tops"]
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        
            model = load_model('model.h5')

            np_image = Image.open(filepath)
            np_image = np_image.resize((64, 64))
            np_image = np.array(np_image) / 255
            np_image = np_image[np.newaxis, :, :, :]
            result = model.predict(np_image)
            #print(result)
            if result[0][0] > result[0][1]:
                return '''
                <!doctype html>
                <html>
                <head>
                <meta charset="UTF-8">
                <title>result</title></head>
                <body>
                <h1>result</h1>
                <p>pants</p>
                </body>
                </html>
                '''
            else :
                return '''
                <!doctype html>
                <html>
                <head>
                <meta charset="UTF-8">
                <title>result</title></head>
                <body>
                <h1>result</h1>
                <p>tops</p>
                </body>
                </html>
                '''
            #return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>ファイルをアップロードして判定しよう</title></head>
    <body>
    <h1>ファイルをアップロードして判定しよう！</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

## おまじない
if __name__ == "__main__":
    app.run(debug=True)