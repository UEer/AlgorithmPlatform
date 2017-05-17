# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, send_from_directory,jsonify
from werkzeug import secure_filename
from im import im_txt

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.getcwd()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# html = '''
#     <!DOCTYPE html>
#     <title>Upload File</title>
#     <h1>图片上传</h1>
#     <form method=post enctype=multipart/form-data>
#          <input type=file name=file>
#          <input type=submit value=上传>
#     </form>
#     '''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/api', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_url = url_for('uploaded_file', filename=filename)
            gen = im_txt.Im2txt()
            result = list(gen.main(filename))
            return jsonify(result)
    else:
        return {'False'}


if __name__ == '__main__':
    app.run('0.0.0.0',port=8888)
#api 测试
# url = 'http://httpbin.org/post'
# files = {'file': open('report.xls', 'rb')}
#
# r = requests.post(url, files=files)
# r.text
