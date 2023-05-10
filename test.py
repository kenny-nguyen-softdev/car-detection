# from ultralytics import YOLO
# import cv2 as cv
# model = YOLO('model_bien_so.pt')
# video_path = "./Videos/video70.mp4"
# cap = cv.VideoCapture(video_path)
# width_video = int(cap.get(3))
# height_video = int(cap.get(4))
# size_of_video = (width_video, height_video)
# video_save = cv.VideoWriter(
#     "./Videos/video4.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
# while cap.isOpened():
#     success, frame = cap.read()
#     if success:
#         results = model(frame)
#         annotated_frame = results[0].plot()
#         # video_save.write(annotated_frame)
#         cv.imshow("Video", annotated_frame)
#         if cv.waitKey(10) & 0xFF == ord('q'):
#             break
#     else:
#         break
# cap.release()
# video_save.release()
# cv.destroyAllWindows()
import cv2 as cv
from ultralytics import YOLO
import numpy as np
import time

model = YOLO('model_bien_so.pt')
video_path = "./Videos/video70.mp4"
cap = cv.VideoCapture(video_path)
width_video = int(cap.get(3))
height_video = int(cap.get(4))
size_of_video = (width_video, height_video)
video_save = cv.VideoWriter(
    "./Videos/video4.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
count = 0
start_time = time.time()
while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame)
        for r in results[0].boxes.data.tolist():
            # print(r)
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            image_car = np.array(results[0].orig_img)
            count += 1
            # Tu anh goc cat anh co chua bien so co toa do (x1:x2,y1:y2)
            new_img = image_car[y1:y2, x1:x2]
            cv.imwrite("new_image" + str(count) + ".png", new_img)
        # annotated_frame = results[0].plot()
        # video_save.write(annotated_frame)
        # print(results[0].orig_img.shape)
        # if cv.waitKey(10) & 0xFF == ord('q'):
        #     break
    else:
        break
end_time = time.time() - start_time
print("Time to run code is: " + str(end_time))
cap.release()
video_save.release()
cv.destroyAllWindows()
