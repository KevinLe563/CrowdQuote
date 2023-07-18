import cv2
import numpy as np
from pathlib import Path
import configparser

# Partially sourced from https://github.com/arunponnusamy/object-detection-opencv/tree/master

def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h, classes, COLORS):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Read values from config

def classify_image(config_path, image_path):
    config = configparser.ConfigParser()
    config.read(config_path)

    yolo_classes_path = str(Path(config_path, config['YOLO']['classes']).resolve())
    yolo_weights_path = str(Path(config_path, config['YOLO']['weights']).resolve())
    yolo_config_path = str(Path(config_path, config['YOLO']['config']).resolve())

    image = cv2.imread(str(image_path))
    width = image.shape[1]
    height = image.shape[0]
    scale = 0.00392

    classes = None
    with open(yolo_classes_path, 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(yolo_weights_path, yolo_config_path)

    blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4


    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        try:
            box = boxes[i]
        except:
            i = i[0]
            box = boxes[i]
        
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h), classes, COLORS)

    # Make window fullscreen
    # cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
    # cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    resized = cv2.resize(image, (1200, 700))
    cv2.imshow("object detection", resized)
    cv2.waitKey()
        
    cv2.imwrite("object-detection.jpg", image)
    cv2.destroyAllWindows()


# For reference for videos:
def video_capture(video_path: str):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        print("failed to open video")

    while cap.isOpened():
        success, frame = cap.read()
        if success:
            frame = cv2.resize(frame, (1200, 700))
            cv2.imshow("Frame", frame)
            
            k = cv2.waitKey(0) & 0xFF # If you want to go one frame at a time
            # k = cv2.waitKey(1) & 0xFF # Plays video with 1 millisec between frames
            
            # Break when ESC key is pressed
            if k == 27:
                cv2.destroyAllWindows()
                print("user pressed ESC")
                break
        else:
            print("failed to get frame or video finished playing")
            break

    cap.release()
    cv2.destroyAllWindows()


# For video
# mod_path = Path(__file__).parent
# video_path = (mod_path / "../resources/person_back_view.mp4").resolve()
# video_capture(video_path)