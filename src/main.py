import cv2
from pathlib import Path
import configparser
from frames import saveFrames
from object_detection import classify_image

config_path = str((Path(__file__).parent / "config.ini").resolve())
config = configparser.ConfigParser()
config.read(config_path)

# saveFrames(config_path, "video2")

image_path = str(Path(config_path, config['IMAGES']['vid2_frame']).resolve())

classify_image(config_path, image_path)

cv2.destroyAllWindows()