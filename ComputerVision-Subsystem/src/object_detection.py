from ultralytics import YOLO
from person import PersonObject
from http_django import update_population
from collections import defaultdict
import cv2
import math
import os
import time
import numpy as np
import subprocess


# credit: https://github.com/MuhammadMoinFaisal/Computervisionprojects/blob/main/YOLOv8-CrashCourse/Running_YOLOv8_Video/YOLOv8_Video.py
# credit: https://github.com/saimj7/People-Counting-in-Real-Time/tree/master

class ObjectDetector():
    def __init__(self, location_id):
        self.location_id = location_id

        # self.model = "~/FYDP/best.pt" # folder for pi
        self.model = "./../training/train21/weights/best.pt"
        # self.model = "./../yolo/yolov8x.pt"

        self.server_url = "http://127.0.0.1:8000/api/population/"
        self.classes = [
                "person", "pedestrian", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                "teddy bear", "hair drier", "toothbrush"
            ] # all avaialble classes of the model, only person is used
        
        self.pts = []
        self.tracked_persons = {}
        self.people_count = 0
        self.entrance_points = None

        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)


    def detectObject(self, entrance_height=None, centroid_radius=5):
        frame_width=1080
        frame_height=720

        model=YOLO(self.model)

        try:
            while True:
                # subprocess.run(["libcamera-jpeg", "-o", "test_images/test.jpg"])

                img = self.poll_image()
                height, width, channels = img.shape
                self.img_height = height
                self.img_width = width
                self.draw_grid(img, height, width)
                cv2.namedWindow("Image")
                results=model.predict(img, stream=True, classes=[0])
                
                # check each bounding box -> draw a rectangle and label it
                count = 0
                # {"row col" : count}
                grid = defaultdict(list)
                for r in results:
                    boxes=r.boxes
                    for box in boxes:
                        object_class=int(box.cls[0])
                        conf=math.ceil((box.conf[0]*100))/100
                        print("Confidence: ", conf)
                        class_name=self.classes[object_class]
                        if (class_name == self.classes[0] or class_name == self.classes[1]) and conf >= 0: # check if it's a person, ignore other objects
                            count +=1

                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            centroid = (int((x2+x1)/2), int((y1+y2)/2))
                            self.classify_grid(centroid[0], centroid[1], height, width, grid)
                            person_object = PersonObject(centroid)
                            self.labelObject(img, self.classes[0], person_object)
                
                self.people_count = count
                self.POST_req(grid)
                print(f"Updated pop: {self.people_count}")
                print(f"Grid: ", grid)
                img = cv2.resize(img, (frame_width, frame_height))
                cv2.imshow("Image", img)
                cv2.waitKey(5000)
                # if cv2.waitKey(1) & 0xFF==ord('q'):
                #     break

                time.sleep(10)
        except Exception as e:
            print(f"Object detection error: {e}")
        cv2.destroyAllWindows()

    def draw_grid(self, img, height, width, rows=4, cols=4):
        dx, dy = width/cols, height/rows

        for i in range(1, cols):
            x = round(dx*i)
            cv2.line(img, (x, 0), (x, height), color=(0, 255, 255), thickness=5)
            
        for i in range(1, rows):
            y = round(dy*i)
            cv2.line(img, (0, y), (width, y), color=(0, 255, 255), thickness=5)

    def classify_grid(self, x, y, height, width, grid, rows=4, cols=4):
        # send cluster # as the key, x y coordinate of point as the value -> each cluster # is unique, can use length of dict

        # dx = width/cols
        # dy = height/rows
        # col = int(x//dx)
        # row = int(y//dy)

        # key = f"{row}  {col}"

        key = len(grid)
        val = [x, y]
        grid[key].append(val)

        return

    def labelObject(self, img, class_name, person_object, color=(255,0,255)):
        cv2.circle(img, person_object.centroids[-1], 15, color, cv2.FILLED)
    
    def POST_req(self, grid):
        # send post req
        print("Sending POST request!")
        print(self.server_url)
        update_population(self.server_url, self.location_id, self.people_count, grid, self.img_height, self.img_width)

    def poll_image(self):
        folder="test_images"
        img = cv2.imread(os.path.join(folder, "test2.jpg"))
        return img