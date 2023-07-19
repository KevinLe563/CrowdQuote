from object_detection import ObjectDetector
from pathlib import Path

import cv2
import configparser


config_path = str((Path(__file__).parent / "config.ini").resolve())
config = configparser.ConfigParser()
config.read(config_path)

image_path = str(Path(config_path, config['VIDEOS']['video6']).resolve())

objectDetector = ObjectDetector(config_path)

objectDetector.detectObject(image_path)