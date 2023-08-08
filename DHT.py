import Adafruit_DHT
import firebase_admin
from firebase_admin import credentials, db
import cv2
import imutils
import time

# initialize the Firebase app with your credentials
cred = credentials.Certificate('baby-data-update-firebase-adminsdk-xsff3-b6ee3dfddc.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testingdht11-default-rtdb.firebaseio.com/'
})

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
 
senddata()
