from ultralytics import YOLO
from pathlib import Path
from object_tracking import Tracker
from person import PersonObject
import cv2
import math
import configparser


# credit: https://github.com/MuhammadMoinFaisal/Computervisionprojects/blob/main/YOLOv8-CrashCourse/Running_YOLOv8_Video/YOLOv8_Video.py

class ObjectDetector():
    def __init__(self, config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.tracker = Tracker()
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
        # tracks set of ids that crossed each line
        crossed_top_line = set()
        crossed_bottom_line = set()

        people_exited = set()
        people_entered = set()

        video_capture=cv2.VideoCapture(video_path)

        frame_width=int(video_capture.get(3))
        frame_height = int(video_capture.get(4))

        output_video=cv2.VideoWriter(f'{self.output_video_path}/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
        model=YOLO(self.model)

        line_entrance_height = entrance_height if entrance_height else frame_height//2
        height_offset = math.ceil(frame_height*0.05)
        top_line_height = line_entrance_height - height_offset
        bottom_line_height = line_entrance_height + height_offset

        try:
            success, img = video_capture.read()
            while success:
                success, img = video_capture.read()
                # do frame by frame for video
                results=model(img,stream=True)
                # draw a line in the center of the image
                self.drawEntranceExitLine(img, (0, top_line_height), (frame_width, top_line_height))
                self.drawEntranceExitLine(img, (0, bottom_line_height), (frame_width, bottom_line_height))
                cv2.putText(img, f'People Entering: {len(people_entered)}', (0, math.ceil(0.2*frame_height)), 0, 1, (0, 255, 0), thickness=1,lineType=cv2.LINE_AA)
                cv2.putText(img, f'People Exiting: {len(people_exited)}', (0, math.ceil(0.3*frame_height)), 0, 1, (0, 255, 0), thickness=1,lineType=cv2.LINE_AA)

                # check each bounding box -> draw a rectangle and label it
                for r in results:
                    person_objects = []
                    boxes=r.boxes
                    for box in boxes:
                        object_class=int(box.cls[0])
                        class_name=self.classes[object_class]
                        if class_name == self.classes[0]: # check if it's a person, ignore other objects
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            person_objects.append((x1, y1, x2, y2))
                    
                    person_objects_with_ids = self.utiliseTracker(person_objects)
                    for person_object_with_id in person_objects_with_ids:
                        x1,y1,x2,y2,id = person_object_with_id

                        bounding_box_width = x2-x1
                        bounding_box_height = y2-y1
                        center_x = x1 + bounding_box_width//2
                        center_y = y1 + bounding_box_height//2

                        self.labelObject(img, self.classes[0], person_object_with_id)
                        # person crosses the top line -> assume top-bottom is exit and bottom-top is enter
                        # tracks people exiting
                        if center_y+centroid_radius > top_line_height and center_y-centroid_radius < top_line_height:
                            crossed_top_line.add(id)
                        if id in crossed_top_line and center_y+centroid_radius > bottom_line_height and center_y-centroid_radius < bottom_line_height:
                            people_exited.add(id)

                        # tracks people entering
                        if center_y+centroid_radius > bottom_line_height and center_y-centroid_radius < bottom_line_height:
                            crossed_bottom_line.add(id)
                        if id in crossed_bottom_line and center_y+centroid_radius > top_line_height and center_y-centroid_radius < top_line_height:
                            people_entered.add(id)

        
                output_video.write(img)
                cv2.imshow("Image", img)
                if cv2.waitKey(1) & 0xFF==ord('q'):
                    break
        except Exception as e:
            print(f"Object detection error: {e}")

        video_capture.release()
        output_video.release()
        cv2.destroyAllWindows()
        print(people_entered)
        print(people_exited)

    def drawEntranceExitLine(self, img, coord1, coord2):
        cv2.line(img, coord1, coord2, (0, 255, 0), thickness=2)

    def labelObject(self, img, class_name, person_object, color=(255,0,255)):
        x1,y1,x2,y2,id = person_object
        cv2.rectangle(img, (x1,y1), (x2,y2), color, 1)
        
        label=f'{class_name} {id}'
        t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=1)[0]
        c2 = x1 + t_size[0], y1 - t_size[1] - 3
        # bounding box
        cv2.rectangle(img, (x1,y1), c2, color, -1, cv2.LINE_AA)  # filled
        # centroid
        bounding_box_width = x2-x1
        bounding_box_height = y2-y1
        center_x = x1 + bounding_box_width//2
        center_y = y1 + bounding_box_height//2
        cv2.circle(img, (center_x, center_y), 5, color, cv2.FILLED)
        # class label
        cv2.putText(img, label, (x1,y1-2),0, 1, (255, 255, 255), thickness=1,lineType=cv2.LINE_AA)
    

    def utiliseTracker(self, person_objects):
        # print(person_objects)
        return self.tracker.update(person_objects)
        

    