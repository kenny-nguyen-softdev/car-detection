import cv2 as cv
from ultralytics import YOLO
import numpy as np
import time
from tracker import *


offset = 6
detec = []
count_car = 0
pos_linha = 550

def pega_centro(x, y, w, h):
    cx = (x + x + w) // 2
    cy = (y + y + h) // 2   
    return cx, cy

model = YOLO('model_bien_so.pt')
video_path = "./Videos/video70.mp4"
cap = cv.VideoCapture(video_path)
# width_video = int(cap.get(3))
# height_video = int(cap.get(4))
# size_of_video = (width_video, height_video)
# video_save = cv.VideoWriter(
#     "./Videos/video4.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
tracker = Tracker()
count = 0
start_time = time.time()
while cap.isOpened():
    success, frame = cap.read()
    list = []
    if success:
        results = model(frame)
        for r in results[0].boxes.data.tolist():
            count +=1
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            print("Gia tri cua r la :")
            print(r)
            # list.append([x1, y1, x2, y2])
            # bbox_id = tracker.update(list)
            # # print(bbox_id)
            # for bbox in bbox_id:
            #     x3, y3, x4, y4, id = bbox
            #     cx = int(x3 + x4) // 2
            #     cy = int(y3 + y4) // 2
            #     print("Gia tri cua cx la: " +str(cx))
            #     print("Gia tri cua cx la: " +str(cy))
            centro = pega_centro(x1, y1, x2, y2)
            detec.append(centro)
        for (x, y) in detec:
            if y < (pos_linha+offset) and y > (pos_linha-offset):
                count_car += 1
                cv2.line(frame1, (25, pos_linha),
                         (1200, pos_linha), (0, 127, 255), 3)
                detec.remove((x, y))
                print("car is detected : "+str(carros))

    else:
        break