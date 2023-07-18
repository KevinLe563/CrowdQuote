from ultralytics import YOLO
from pathlib import Path
import cv2
import math
import configparser

# credit: https://github.com/MuhammadMoinFaisal/Computervisionprojects/blob/main/YOLOv8-CrashCourse/Running_YOLOv8_Video/YOLOv8_Video.py

class ObjectDetector():
    def __init__(self,config_path):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

        self.model = str(Path(self.config['YOLO']['yolov8n']))
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
        
    def detectObject(self, video_path):
        video_capture=cv2.VideoCapture(video_path)

        frame_width=int(video_capture.get(3))
        frame_height = int(video_capture.get(4))

        output_video=cv2.VideoWriter(f'{self.output_video_path}/output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))
        model=YOLO(self.model)

        while True:
            success, img = video_capture.read()
            # do frame by frame for video
            results=model(img,stream=True)
            # draw a line in the center of the image
            cv2.line(img, (0, frame_height//2), (frame_width, frame_height//2), (0, 255, 0), thickness=2)

            # check each bounding box -> draw a rectangle and label it
            for r in results:
                boxes=r.boxes
                for box in boxes:
                    object_class=int(box.cls[0])
                    class_name=self.classes[object_class]
                    if class_name == self.classes[0]: # ignore other objects
                        x1,y1,x2,y2=box.xyxy[0]
                        x1,y1,x2,y2=int(x1), int(y1), int(x2), int(y2)
                        cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,255),3)
                        
                        label=f'{class_name}'
                        t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                        c2 = x1 + t_size[0], y1 - t_size[1] - 3
                        cv2.rectangle(img, (x1,y1), c2, [255,0,255], -1, cv2.LINE_AA)  # filled
                        cv2.putText(img, label, (x1,y1-2),0, 1,[255,255,255], thickness=1,lineType=cv2.LINE_AA)
            output_video.write(img)
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF==ord('q'):
                break

        video_capture.release()
        output_video.release()
        cv2.destroyAllWindows()
