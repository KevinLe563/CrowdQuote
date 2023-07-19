from ultralytics import YOLO
from pathlib import Path
from object_tracking import CentroidTracker
from person import PersonObject
import numpy as np
import cv2
import math
import configparser


# credit: https://github.com/MuhammadMoinFaisal/Computervisionprojects/blob/main/YOLOv8-CrashCourse/Running_YOLOv8_Video/YOLOv8_Video.py

class ObjectDetector():
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.tracker = CentroidTracker()
        self.model = str(Path(self.config['YOLO']['yolov8model']))
        self.output_video_path = str(Path(config_path, self.config['VIDEOS']['output_videos']).resolve())
        self.classes = [
                "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
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
        
    def detectObject(self, video_path, entrance_height=None, centroid_radius=5):
        tracked_persons = {}
        total_entering = 0
        total_exiting = 0

        video_capture=cv2.VideoCapture(video_path)

        frame_width=int(video_capture.get(3))
        frame_height = int(video_capture.get(4))

        output_video=cv2.VideoWriter(f'{self.output_video_path}/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
        model=YOLO(self.model)

        line_entrance_height = entrance_height if entrance_height else frame_height//2

        try:
            success, img = video_capture.read()
            while success:
                success, img = video_capture.read()
                # do frame by frame for video
                results=model(img,stream=True)
                # draw a line in the center of the image
                self.drawEntranceExitLine(img, (0, line_entrance_height), (frame_width, line_entrance_height))
                cv2.putText(img, f'People Entering: {total_entering}', (0, math.ceil(0.2*frame_height)), 0, 1, (0, 255, 0), thickness=1,lineType=cv2.LINE_AA)
                cv2.putText(img, f'People Exiting: {total_exiting}', (0, math.ceil(0.3*frame_height)), 0, 1, (0, 255, 0), thickness=1,lineType=cv2.LINE_AA)

                # check each bounding box -> draw a rectangle and label it
                for r in results:
                    person_rects = []
                    boxes=r.boxes
                    for box in boxes:
                        object_class=int(box.cls[0])
                        class_name=self.classes[object_class]
                        if class_name == self.classes[0]: # check if it's a person, ignore other objects
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            person_rects.append((x1, y1, x2, y2))
                    
                    person_objects = self.utiliseTracker(person_rects)
                    for (objectID, centroid) in person_objects.items():
                        person_object = tracked_persons.get(objectID, None)

                        if not person_object:
                            person_object = PersonObject(objectID, centroid)
                        else:
                            # the difference between the y-coordinate of the *current*
                            # centroid and the mean of *previous* centroids will tell
                            # us in which direction the object is moving (negative for
                            # 'up' and positive for 'down')

                            # c[1] is the y value of centroid
                            y = [c[1] for c in person_object.centroids]
                            direction = centroid[1] - np.mean(y)
                            person_object.centroids.append(centroid)

                            # check to see if the object has been counted or not
                            if not person_object.is_counted:
                                # if the direction is negative (indicating the object
                                # is moving up and entering) AND the centroid is above the center
                                # line, count the object
                                if direction < 0 and centroid[1] < line_entrance_height:
                                    total_entering += 1
                                    person_object.is_counted = True

                                # if the direction is positive (indicating the object
                                # is moving down and is exiting) AND the centroid is below the
                                # center line, count the object
                                elif direction > 0 and centroid[1] > line_entrance_height:
                                    total_exiting += 1
                                    person_object.is_counted = True
                            
                        # store the trackable object in our dictionary
                        tracked_persons[objectID] = person_object
                        print(person_object.centroids[0])
                        self.labelObject(img, self.classes[0], person_object)
                                    
        
                output_video.write(img)
                cv2.imshow("Image", img)
                print('===')
                if cv2.waitKey(1) & 0xFF==ord('q'):
                    break
        except Exception as e:
            print(f"Object detection error: {e}")

        video_capture.release()
        output_video.release()
        cv2.destroyAllWindows()

    def drawEntranceExitLine(self, img, coord1, coord2):
        cv2.line(img, coord1, coord2, (0, 255, 0), thickness=2)

    def labelObject(self, img, class_name, person_object, color=(255,0,255)):
        # x1,y1,x2,y2,id = person_object
        # cv2.rectangle(img, (x1,y1), (x2,y2), color, 1)
        
        label=f'{class_name} {person_object.objectID}'
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
        

    