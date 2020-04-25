import os
from flask import Flask, render_template, url_for, request, flash, redirect, send_file
from werkzeug.utils import secure_filename
from flask import send_from_directory
from PIL import Image
from pydub import AudioSegment
UPLOAD_FOLDER = ""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename,ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert(filename,type):
    if type =='image':
        im1 = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file = os.path.splitext(filename)[0] + ".png"
        im1.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
    if type =='audio':
        sound = AudioSegment.from_mp3(filename)
        file = os.path.splitext(filename)[0] + ".wav"
        sound.export(file, format="wav")

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/image",methods=['GET', 'POST'])
def image():
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
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
        if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            convert(filename,type="image")
            file = os.path.splitext(filename)[0] + ".png"
            #return redirect(url_for('uploaded_file',filename=file))
            return render_template('success.html', filename = file)

    return render_template('image.html')

@app.route("/audio",methods=['GET', 'POST'])
def audio():
    ALLOWED_EXTENSIONS = {'mp3'}
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
        if file and allowed_file(file.filename,ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            convert(filename,type = "audio")
            file = os.path.splitext(filename)[0] + ".wav"
            #return redirect(url_for('uploaded_file',filename=file))
            return render_template('success.html', filename = file)

    return render_template('image.html')
@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/download/<filename>')
def download(filename):
	return send_file(filename, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)