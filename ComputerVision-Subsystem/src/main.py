from object_detection import ObjectDetector
from pathlib import Path
import numpy as np

import cv2
import configparser


config_path = str((Path(__file__).parent / "config.ini").resolve())
config = configparser.ConfigParser()
config.read(config_path)

image_path = str(Path(config_path, config['IMAGES']['office']).resolve())
image = cv2.imread(image_path)

def onClick(event,x,y,flags,param):
    """Called whenever user left clicks"""
    global Running
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'I saw you click at {x},{y}')
        Running = False
wname = 'img'
cv2.namedWindow(winname=wname)
cv2.setMouseCallback(wname, onClick)
image = cv2.resize(image, (1080, 720))
# cv2.line(image, (0, 10), (100, 5), (0, 255, 0), thickness=2)
pts = np.array([[509,559], [573,620], [562,171], [493,182]])
cv2.polylines(image, [pts], True, (0, 255, 0), thickness=2)
cv2.imshow(wname, image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# objectDetector = ObjectDetector(config_path, 1)

# objectDetector.detectObject(image_path)