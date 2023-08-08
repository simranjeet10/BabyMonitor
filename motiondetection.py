import cv2
import imutils
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time

# Set up the Firebase credentials and initialize the app
cred = credentials.Certificate(r'baby-data-update-firebase-adminsdk-xsff3-b6ee3dfddc.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://testingdht11-default-rtdb.firebaseio.com/'
})

# Get a reference to the movement status node in the Realtime Database
movement_ref = db.reference('movement_status')

# Set up the video capture device
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Read the starting frame and perform some preprocessing
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

def motion_check():
    global start_frame

    while True:
        _, frame = cap.read()
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
            movement_ref.set(Message)

        # Check for the 'q' key to quit the loop
        key = cv2.waitKey(100) & 0xFF
        if key == ord('q'):
            break

    # Release the camera and close the window
    cap.release()
    cv2.destroyAllWindows()
motion_check()
