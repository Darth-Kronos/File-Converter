import os
from flask import Flask, render_template, url_for, request, flash, redirect, send_file
from werkzeug import secure_filename
from flask import send_from_directory
from PIL import Image

UPLOAD_FOLDER = "/home/puru/Documents/College/6_sem/CN/"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert(filename):
    im1 = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file = os.path.splitext(filename)[0] + ".png"
    im1.save(os.path.join(app.config['UPLOAD_FOLDER'], file))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            convert(filename)
            file = os.path.splitext(filename)[0] + ".png"
            return redirect(url_for('uploaded_file',
                                    filename=file))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route("/uploaded_file")
def uploaded_file():
    filename = request.args.get('filename',None)
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'],
                                filename),as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)