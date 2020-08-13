from cv2 import cv2
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
camera = cv2.VideoCapture(0)
@app.route('/', methods=["GET", "POST"])
def get_frame():

    # recieve message from electron app
    if request.method == "POST":
        json_message = request.get_json()
        print(json_message)         # data recieved from electron app as strings

    # send data to the electron app
    frame = "-"
    bluetooth = []
    while True:
        #get camera frame
        ret, frame = camera.read()
        frame=cv2.resize(frame,None,fx=0.6,fy=0.6, interpolation=cv2.INTER_AREA)                    
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        encoded = jpeg.tobytes()
        encoded = base64.b64encode(encoded).decode('ascii')
        return jsonify(frame=encoded, bluetooth=bluetooth)

    
    
    
    return jsonify(frame=frame, bluetooth=bluetooth)


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port=5000, debug=False)
