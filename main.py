from flask import Flask, render_template, Response
import cv2
import DHT as dht
from threading import Thread

app = Flask(__name__)
camera = cv2.VideoCapture(1)

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        ret, frame = self.video.read()
        return cv2.imencode('.jpg', frame)[1].tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def main():
    return render_template('index.html')
@app.before_first_request
def initialize():
    t2=Thread(target=dht.senddata)
    t2.start()

if __name__ == "__main__":
     app.run(host='0.0.0.0', port='5000', debug=True)
