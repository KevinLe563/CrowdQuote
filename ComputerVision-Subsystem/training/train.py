# %%
from ultralytics import YOLO
import torch
# %%

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# Load a model
model = YOLO('yolov8n.pt').to(device)  # load a pretrained model (recommended for training)

# Train the model
results = model.train(data='./VisDrone.yaml', epochs=5, imgsz=640)


