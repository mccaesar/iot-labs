from get_laptop_camera import get_laptop_camera
from cv2 import cv2
import base64
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
camera = cv2.VideoCapture(0)        
@app.route('/', methods=["GET", "POST"])
def get_frame():

    # send data to the electron app
    _frame = "-"
    _bluetooth = []
    json_message = ""

    # recieve message from electron app
    if request.method == "POST":
        json_message = request.get_json()
        print(json_message)         # data recieved from electron app as strings
        
    encoded = get_laptop_camera(camera)
    _frame = encoded

    # if json_message != "get_video":
    #     _frame = "-"
    
    return jsonify(frame=_frame, bluetooth=_bluetooth)


if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port=5000, debug=False)
