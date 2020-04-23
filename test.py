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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/image",methods=['GET', 'POST'])
def image():
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
    return render_template('image.html')
@app.route('/success')
def success():
    return render_template('success.html')
@app.route('/download')
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "simple.docx"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)
if __name__ == '__main__':
    app.run(debug=True)