
from flask import Flask, render_template, Response
import cv2
import Adafruit_DHT
import imutils
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from threading import Thread

# Set up the Firebase credentials and initialize the app
cred = credentials.Certificate(r'baby-data-update-firebase-adminsdk-xsff3-b6ee3dfddc.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://testingdht11-default-rtdb.firebaseio.com/'})

# specify the database path where you want to write the data
temp_ref = db.reference('Weather/Temp')
humid_ref = db.reference('Weather/Humid')

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 2

def senddata():
    while True:
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
            temp_ref.set(temperature)
            humid_ref.set(humidity)
        else:
            print("Sensor failure. Check wiring.")
        time.sleep(60)

# Get a reference to the movement status node in the Realtime Database
movement_ref = db.reference('movement_status')

# Set up the video capture device
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Read the starting frame and perform some preprocessing
_, start_frame = camera.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

def run_motion_detection():
    global start_frame
    while True:
        _, frame = camera.read()
        frame = imutils.resize(frame, width=500)
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (21, 21), 0)
        diff = cv2.absdiff(start_frame, frame_bw)
        thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw
        if thresh.sum() > 1000000:
            Message = "Movement Detected"
            print("motion detected")
            movement_ref.set(Message)
        else:
            Message = "No Movement"
            print("not detected")
       # Check for the 'q' key to quit the loop
        key = cv2.waitkey(100) &	0xFF
        if key == ord('q'):
            break	

# Release the camera and close the window
camera.release()
cv2.destroyAllWindows()

app = Flask(__name__)

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
    t2=Thread(target=senddata)
    t2.start()
if __name__ == "__main__":
     app.run(host='0.0.0.0', port='5000', debug=True)

           

