from ultralytics import YOLO
from pathlib import Path
from object_tracking import CentroidTracker
from person import PersonObject
from http_django import update_population
from person_state import PersonState
import numpy as np
import cv2
import math
import configparser
import sched
import os
import time
import subprocess


# credit: https://github.com/MuhammadMoinFaisal/Computervisionprojects/blob/main/YOLOv8-CrashCourse/Running_YOLOv8_Video/YOLOv8_Video.py
# credit: https://github.com/saimj7/People-Counting-in-Real-Time/tree/master

class ObjectDetector():
    def __init__(self, location_id, time_per_POST=5):
        # self.config = configparser.ConfigParser()
        # self.config.read(config_path)
        self.location_id = location_id
        self.time_per_POST = time_per_POST
        # self.population_scheduler = sched.scheduler(time.time, time.sleep)

        self.tracker = CentroidTracker()
        self.model = "~/FYDP/best.pt"
        # self.output_video_path = str(Path(config_path, self.config['VIDEOS']['output_videos']).resolve())
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

        # output_video=cv2.VideoWriter(f'{self.output_video_path}/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
        model=YOLO(self.model)

        try:
            while True:
                # time.sleep(10)
                subprocess.run(["libcamera-jpeg", "-o", "test_images/test.jpg"])
                # self.population_scheduler.enter(self.time_per_POST, 1, self.POST_scheduler, (self.population_scheduler,))
                img = self.poll_image()
                # for img in imgs: # TODO: replace this with a busy poll from raspberry pi
                # self.population_scheduler.run(blocking=False)
                img = cv2.resize(img, (frame_width, frame_height))
                cv2.namedWindow("Image")
                # self.drawBounds(img)
                # do frame by frame for video
                results=model.predict(img, stream=True, classes=[0])
                # self.drawEntranceExitBox(img, entranceCoord1, entranceCoord2)
                
                # check each bounding box -> draw a rectangle and label it
                count = 0
                for r in results:
                    boxes=r.boxes
                    for box in boxes:
                        object_class=int(box.cls[0])
                        conf=math.ceil((box.conf[0]*100))/100
                        print("Confidence: ", conf)
                        class_name=self.classes[object_class]
                        if (class_name == self.classes[0] or class_name == self.classes[1]) and conf >= 0.6: # check if it's a person, ignore other objects
                            count +=1

                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            centroid = (int((x2+x1)/2), int((y1+y2)/2))
                            person_object = PersonObject(centroid)
                            self.labelObject(img, self.classes[0], person_object)
                
                if self.people_count != count:
                    self.people_count = count
                    update_population(self.server_url, self.location_id, self.people_count)
                    print(f"Updated pop: {self.people_count}")

                # output_video.write(img)
                cv2.imshow("Image", img)
                if cv2.waitKey(1) & 0xFF==ord('q'):
                    break
                time.sleep(10)
        except Exception as e:
            print(f"Object detection error: {e}")
        cv2.destroyAllWindows()

    def drawEntranceExitLine(self, img, coord1, coord2):
        cv2.line(img, coord1, coord2, (0, 255, 0), thickness=2)

    def drawEntranceExitBox(self, img, coord1, coord2):
        # cv2.rectangle(img, coord1, coord2, (0, 255, 0), thickness=2)
        cv2.polylines(img, [self.entrance_points], True, (0, 255, 0), thickness=2)

    def labelObject(self, img, class_name, person_object, color=(255,0,255)):
        # x1,y1,x2,y2,id = person_object
        # cv2.rectangle(img, (x1,y1), (x2,y2), color, 1)
        
        label=f'{class_name}'
        # t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=1)[0]
        # c2 = x1 + t_size[0], y1 - t_size[1] - 3
        # bounding box
        # cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
        # centroid
        # bounding_box_width = x2-x1
        # bounding_box_height = y2-y1
        # center_x = x1 + bounding_box_width//2
        # center_y = y1 + bounding_box_height//2
        cv2.circle(img, person_object.centroids[-1], 5, color, cv2.FILLED)
        # class label

        cv2.putText(img, label, (person_object.centroids[-1][0], person_object.centroids[-1][1]-2), 0, 1, (255, 255, 255), thickness=1,lineType=cv2.LINE_AA)
    

    def utiliseTracker(self, person_objects):
        # print(person_objects)
        return self.tracker.update(person_objects)
        
    # used to reset the system when the camera is off
    def reset(self):
        self.tracker.reset()
        self.tracked_persons = {}

    def POST_req(self, scheduler):
        # schedule the next call first
        # scheduler.enter(self.time_per_POST, 1, self.POST_scheduler, (scheduler,))

        # send post req
        print("Sending POST request!")
        print(self.server_url)
        update_population(self.server_url, self.location_id, self.people_count)

    def detect_click(self, event,x,y,flags,param):
        """Called whenever user left clicks"""
        if event == cv2.EVENT_LBUTTONDOWN:
            print(f'I saw you click at {x},{y}')
            self.pts.append([x, y])

    def drawBounds(self, img):
        if len(self.pts) >= 4:
            return
        cv2.imshow("Image", img)
        cv2.setMouseCallback('Image', self.detect_click)
        while len(self.pts) < 4:
            k = cv2.waitKeyEx(1)
        cv2.setMouseCallback('Image', lambda *args : None)
        self.entrance_points = np.array(self.pts)
        self.tracker.updateEntranceBounds(self.entrance_points)

    def poll_image(self):
        # TODO: change this later to poll image from the raspberry PI camera
        images = []
        folder="test_images"
        # for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, "test.jpg"))
        
        # if img is not None:
        #     images.append(img)

        # temp = max(images, key=os.path.getmtime)
        # print(temp)

        # return images[0]
        return img

        # return max(valid_files, key=os.path.getmtime) 
