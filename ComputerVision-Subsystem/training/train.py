# %%
from ultralytics import YOLO

# %%


# Load a model
model = YOLO('yolov8s.pt')  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='./VisDrone.yaml', epochs=100, imgsz=640)


