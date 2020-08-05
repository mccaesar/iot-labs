import picamera
import numpy as np 

from PIL import Image
from tflite_runtime.interpreter import Interpreter
import re,io
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

class HouserBoon:
    args = {
        "labels": "/tmp/coco_labels.txt",
        "model": "/tmp/detect.tflite",
        "threshold": .4
    }

    def load_labels(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            labels = {}
            for row_number, content in enumerate(lines):
                pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)
                if len(pair) == 2 and pair[0].strip().isdigit():
                    labels[int(pair[0])] = pair[1].strip()
                else:
                    labels[row_number] = pair[0].strip()
        return labels


    def __init__(self):
        self.labels = self.load_labels(self.args["labels"])
        self.interpreter = Interpreter(self.args["model"])
        self.interpreter.allocate_tensors()
        _, self.input_height, self.input_width, _ = self.interpreter.get_input_details()[0]['shape']

    def set_input_tensor(self, interpreter, image):
        """Sets the input tensor."""
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def get_output_tensor(self, interpreter, index):
        """Returns the output tensor at the given index."""
        output_details = interpreter.get_output_details()[index]
        tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
        return tensor


    def detect_objects(self, interpreter, image, threshold):
        """Returns a list of detection results, each a dictionary of object info."""
        self.set_input_tensor(interpreter, image)
        self.interpreter.invoke()

        # Get all output details
        boxes = self.get_output_tensor(self.interpreter, 0)
        classes = self.get_output_tensor(self.interpreter, 1)
        scores = self.get_output_tensor(self.interpreter, 2)
        count = int(self.get_output_tensor(self.interpreter, 3))

        results = []
        for i in range(count):
            if scores[i] >= threshold:
                result = {
                    'bounding_box': boxes[i],
                    'class_id': classes[i],
                    'score': scores[i]
                }
                results.append(result)
        return results
    
    def show_us_the_bolt(self):
        with picamera.PiCamera(resolution=(CAMERA_WIDTH, CAMERA_HEIGHT), framerate=30) as camera:
            camera.start_preview()
            try:
                stream = io.BytesIO()
                camera.capture(stream, format = "jpeg")
                stream.seek(0)
                image = Image.open(stream).convert('RGB').resize(
                    (self.input_width, self.input_height), Image.ANTIALIAS)

                results = self.detect_objects(self.interpreter, image, self.args["threshold"])
                for obj in results:
                    if self.labels[obj['class_id']] == "person" or self.labels[obj['class_id']] == "stop sign":
                        return True


                stream.seek(0)
                stream.truncate()

            finally:
                camera.stop_preview()
        return False


cam = HouserBoon()
print(cam.show_us_the_bolt())


import numpy as np 
import math
import pprint
import heapq
import time
from picar_4wd.pin import Pin
from picar_4wd.pwm import PWM 
from picar_4wd.ultrasonic import Ultrasonic 
from picar_4wd.utils import mapping
from picar_4wd.servo import Servo
from picar_4wd.speed import Speed
import picar_4wd as fc



class LightningMcqueen:
    ser = Servo(PWM("P0"))
    us = Ultrasonic(Pin("D8"), Pin("D9"))
    angle_increment = 5
    length_per_position = 2.5 #5 cm / position in numpy array
    houser_boon = HouserBoon()
    target = (150, 150)
    direction = 0

    def __init__(self, target):
        self.target = target
        self.map_to_fill = np.zeros((150, 150))
        self.position = (self.map_to_fill.shape[0]*.5, 0)
        self.rescan_limit = 10

    def findMove(current, prev):
        if current[1] == prev[1] + 1:
            return "forward"
        if current[0] == prev[0] + 1:
            return "down"
        if current[0] == prev[0] - 1:
            return "up"

    def lets_do_this_thing(self, map_to_fill):
        map_to_fill = scan_and_build_map(60, map_to_fill)
        np.set_printoptions(threshold=np.inf)
        printmat(map_to_fill.astype(int))

        start = (map_to_fill.shape[0]*.5, 0)
        rec = a_star_recommendation(map_to_fill, self.target)
        

        start = self.position

        starting_coordinate = self.position

        direction = self.direction
        prev = starting_coordinate


        # def turnRight():
        #     print("right")
        # def turnLeft():
        #     print("left")
        # def move25(): 
        #     print("forward")

        # direction 0 = east
        # direction 1 = south
        # direction -1 = north
        for i in range(min(len(rec), self.rescan_limit)):
            coordinate = rec[i]

            while (houser_boon.show_us_the_bolt()):
                time.sleep(3)
                print("STOP") 
            if direction == 0 and findMove(coordinate, prev) == "forward":
                move25()
                self.position[0] += self.length_per_position

            elif direction == 1 and findMove(coordinate, prev) == "forward":
                turnLeft()
                move25()
                direction = 0
                self.position[0] += self.length_per_position

            elif direction == -1 and findMove(coordinate, prev) == "forward":
                turnRight()
                move25()
                direction = 0
                self.position[0] += self.length_per_position

            if direction == 0 and findMove(coordinate, prev) == "down":
                turnRight()
                move25()
                direction = 1
                self.position[1] -= self.length_per_position

            elif direction == 1 and findMove(coordinate, prev) == "down":
                move25()
                self.position[1] -= self.length_per_position

            elif direction == -1 and findMove(coordinate, prev) == "down":
                turnRight()
                turnRight()
                move25()
                direction = 1
                self.position[1] -= self.length_per_position

            elif direction == 0 and findMove(coordinate, prev) == "up":
                turnLeft()
                move25()
                direction = -1
                self.position[1] += self.length_per_position

            elif direction == 1 and findMove(coordinate, prev) == "up":
                turnLeft()
                turnLeft()
                move25()
                direction = -1
                self.position[1] += self.length_per_position

            elif direction == -1 and findMove(coordinate, prev) == "up":
                move25()
                self.position[1] += self.length_per_position
            
            map_to_fill[int(coordinate[0]), coordinate[1]] = 6
            prev = coordinate
        self.target[0] -= position[0]
        self.target[1] -= position[1]
        self.direction = direction
            
    def kachow(self):
        while(lets_do_this_thing(self.map_to_fill)):
            print("Scanned")

    def move25():
        speed4 = Speed(25)
        speed4.start()
        # time.sleep(2)
        fc.backward(100)
        x = 0
        for i in range(1):
            time.sleep(0.1)
            speed = speed4()
            x += speed * 0.1
            print("%smm/s"%speed)
        print("%smm"%x)
        speed4.deinit()
        fc.stop()

    def turnLeft():
        speed4 = Speed(25)
        speed4.start()
        # time.sleep(2)
        fc.turn_right(80)
        x = 0
        for i in range(6):
            time.sleep(0.1)
            speed = speed4()
            x += speed * 0.1
            print("%smm/s"%speed)
        print("%smm"%x)
        speed4.deinit()
        fc.stop()

    def turnRight():
        speed4 = Speed(25)
        speed4.start()
        # time.sleep(2)
        fc.turn_left(80)
        x = 0
        for i in range(6):
            time.sleep(0.1)
            speed = speed4()
            x += speed * 0.1
            print("%smm/s"%speed)
        print("%smm"%x)
        speed4.deinit()
        fc.stop()


    def get_distance(angle):
        self.ser.set_angle(angle)
        time.sleep(0.5)
        return self.us.get_distance()

    def scan_and_build_map(angle, map_to_fill):
        last_position = [0,0]
        map_to_fill[0,0] = 7
        map_to_fill[int(len(map_to_fill)*.5), 0] = 5
        for current_angle in range(-1*angle, angle, self.angle_increment):
            current_distance = get_distance(current_angle)
            print(current_distance)
            if current_angle == -1*angle:
                last_position = [(len(map_to_fill)*.5 - current_distance*math.sin(math.radians(current_angle)))/self.length_per_position, current_distance*math.cos(math.radians(current_angle))/self.length_per_position]
                if (last_position[0] < len(map_to_fill) and last_position[1] <= len(map_to_fill)):
                    map_to_fill[int(last_position[0]), int(last_position[1])] = 1
            else:
                current_position = [len(map_to_fill)*.5 - current_distance*math.sin(math.radians(current_angle))/self.length_per_position, current_distance*math.cos(math.radians(current_angle))/self.length_per_position]
                if (current_position[0] < len(map_to_fill) and current_position[1] <= len(map_to_fill)):
                    map_to_fill[int(current_position[0]), int(current_position[1])] = 1
                    slope = (current_position[1] - last_position[0])/(current_position[0] - last_position[0])
                    for i in range(0, int(current_position[0] - last_position[0])):
                        if (last_position[0] + i < len(map_to_fill) and last_position[1] + i*slope < len(map_to_fill)):
                            map_to_fill[int(last_position[0] + i), int(last_position[1] + i*slope)] = 1
        map_to_fill[int(len(map_to_fill)*.5), 0] = 5
        return map_to_fill
        

    def a_star_recommendation(map_to_fill, target_coordinates):
        open = []
        heapq.heappush(open, (0, start))
        traversal = {}
        cost = {}
        traversal[target_coordinates] = None
        cost[start] = 0
        
        while True:
            print
            curr = heapq.heappop(open)[1]
            if curr == target_coordinates:
                break
            for neighbor in get_possible_moves(map_to_fill, curr):
                neighbor_cost = cost[curr] + 1
                if neighbor not in cost or cost[neighbor] > neighbor_cost:
                    cost[neighbor] = neighbor_cost
                    heapq.heappush(open, (neighbor_cost + h(neighbor, target_coordinates),neighbor))
                    traversal[neighbor] = curr
        back = target_coordinates
        output = []
        while back != None and back in traversal:
            output.append(back)
            back = traversal[back]
        output.reverse()
        return output

    def h(a, b):
        return abs(b[1] - a[1]) + abs(a[0] - b[0])

    def get_possible_moves(map_to_fill, current_coordinate):
        possible_moves = []
        if current_coordinate[0] - 1 >= 0 and map_to_fill[int(current_coordinate[0]) - 1, current_coordinate[1]] != 1:
            possible_moves.append((current_coordinate[0] - 1, current_coordinate[1]))
        if (current_coordinate[0] + 1 < len(map_to_fill) and map_to_fill[int(current_coordinate[0]) + 1, current_coordinate[1]] != 1):
            possible_moves.append((current_coordinate[0] + 1, current_coordinate[1]))
        if (current_coordinate[1] - 1 >= 0 and map_to_fill[int(current_coordinate[0]), current_coordinate[1] - 1] != 1):
            possible_moves.append((current_coordinate[0], current_coordinate[1] - 1))
        if (current_coordinate[1] + 1 < len(map_to_fill[0]) and map_to_fill[int(current_coordinate[0]), current_coordinate[1] + 1] != 1 ):
            possible_moves.append((current_coordinate[0], current_coordinate[1] + 1))
        
        return possible_moves

    def format__1(digits,num):
        if digits<len(str(num)):
            raise Exception("digits<len(str(num))")
        return ' '*(digits-len(str(num))) + str(num)
    def printmat(arr,row_labels=[], col_labels=[]): #print a 2d numpy array (maybe) or nested list
        max_chars = 2
        if row_labels==[] and col_labels==[]:
            for row in arr:
                print('[%s]' %(' '.join(format__1(max_chars,i) for i in row)))
        elif row_labels!=[] and col_labels!=[]:
            rw = max([len(str(item)) for item in row_labels]) #max char width of row__labels
            print('%s %s' % (' '*(rw+1), ' '.join(format__1(max_chars,i) for i in col_labels)))
            for row_label, row in zip(row_labels, arr):
                print('%s [%s]' % (format__1(rw,row_label), ' '.join(format__1(max_chars,i) for i in row)))
        else:
            raise Exception("This case is not implemented...either both row_labels and col_labels must be given or neither.")
            
    def add_clearance(map_to_fill):
        copied_result = np.copy(map_to_fill)
        for i in range(len(map_to_fill)):
            for j in range(len(map_to_fill[0])):
                if (map_to_fill[i, j] == 1):
                    for move in get_possible_moves(map_to_fill, [i, j]):
                        if (copied_result[move[0], move[1]] == 0):
                            copied_result[move[0], move[1]] = 1

        return copied_result






SPEED = LightningMcqueen()

SPEED.kachow()

