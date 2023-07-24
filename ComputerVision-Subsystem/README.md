### YOLOv3
Annoying issue with OpenCV2: can't use pathlib Path objects, need to convert to str https://github.com/opencv/opencv/issues/15731

Please go to https://pjreddie.com/media/files/yolov3.weights to download the weights. Copy this into src directory.

### YOLOv8

1. pip install -r requirements.txt in the ComputerVision-Subsystem directory

2. Run main, it should automatically download the weights if you don't have them locally (run main while you are in ComputerVision-Subsystem subdirectory). Output video will be saved to /resources/output_videos/output.avi