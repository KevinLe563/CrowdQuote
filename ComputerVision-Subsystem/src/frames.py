import cv2
import configparser
from pathlib import Path

def saveFrames(config_path, video_id):
    config = configparser.ConfigParser()
    config.read(config_path)

    resources_path = Path(config['RESOURCES']['path'])
    video_path = Path(config['VIDEOS'][video_id])

    Path((resources_path / video_id)).mkdir(parents=True, exist_ok=True)
    
    cap = cv2.VideoCapture(str(video_path))
    for i in range(10):
        success, frame = cap.read()
        if success:
            output_path = resources_path / f'{video_id}/{video_id}_{i}.jpg'
            cv2.imwrite(str((output_path).resolve()), frame)

config_path = (Path(__file__).parent / "config.ini").resolve()
saveFrames(str(config_path), "video1")