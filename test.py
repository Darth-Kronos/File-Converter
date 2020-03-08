from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO
from werkzeug import secure_filename
UPLOAD_FOLDER = "/home/puru/Documents/College/6_sem/CN/Project/"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')
@app.route("/image")
def image():
    return render_template('image.html')
@app.route('/success',methods = ['GET','POST'])
def success():
    if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
    return render_template('success.html')
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)