from flask import Flask, send_file, render_template
app = Flask(__name__)	
@app.route('/')
def upload_form():
	return '''
    <!doctype html>
    <title>Python Flask File Download Example</title>
    <h2>Download a file</h2>

    <p>
        <a href="{{ url_for('.download_file') }}">Download</a>
    </p>
'''

@app.route('/download')
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "simple.docx"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run()