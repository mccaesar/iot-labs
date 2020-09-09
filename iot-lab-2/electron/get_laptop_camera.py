from cv2 import cv2
import base64

def get_laptop_camera(camera):
    #get camera frame
    ret, frame = camera.read()
    frame=cv2.resize(frame,None,fx=0.6,fy=0.6, interpolation=cv2.INTER_AREA)                    
    # encode OpenCV raw frame to jpg and displaying it
    ret, jpeg = cv2.imencode('.jpg', frame)
    encoded = jpeg.tobytes()
    encoded = base64.b64encode(encoded).decode('ascii')
    return encoded

    