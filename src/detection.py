import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2

model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
img = 'https://nmaahc.si.edu/sites/default/files/styles/max_1300x1300/public/images/header/audience-citizen_0.jpg?itok=unjNTfkP'
results = model(img)
print(results)


cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, frame = cap.read()