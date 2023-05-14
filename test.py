import cv2 as cv
from ultralytics import YOLO
import numpy as np
import time
import os

model = YOLO('model_bien_so.pt')
video_path = "./Videos/video70.mp4"
cap = cv.VideoCapture(video_path)
width_video = int(cap.get(3))
height_video = int(cap.get(4))
size_of_video = (width_video, height_video)
video_save = cv.VideoWriter(
    "./Videos/video4.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
count = 0
detect = []
same_detect = []
n_detect = 0
start_time = time.time()
while cap.isOpened():
    success, frame = cap.read()
    if success:
        results = model(frame)
        for r in results[0].boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)
            image_car = np.array(results[0].orig_img)
            # Tu anh goc cat anh co chua bien so co toa do (x1:x2,y1:y2)
            new_img = image_car[y1:y2, x1:x2]
            detect.append(new_img)
            n_detect +=1
            # if(len(detect) == 1 or (detect[n_detect - 1].all() != detect[n_detect -2].all())):
            #     # print("./new_img/new_image" + str(count) + ".png")
            #     cv.imwrite("./new_img/new_image" + str(count) + ".png", new_img)
            if(len(detect) == 1 or (detect[n_detect - 1].all() != detect[n_detect -2].all())):
                # count += 1
                # print("new_image" +str(count)+ ".png")
                # cv.imwrite("./new_img_license/new_image" +str(count)+ ".png", new_img)
                same_detect.append(detect[n_detect - 1])
            # if(np.isclose(detect[n_detect - 1].shape, detect[n_detect - 2].shape, rtol=10, atol=10).all()):
            #     if(os.path.isfile("./new_img_license/new_image" +str(count)+ ".png")):
            #         print("ANh da bi xoa")
            #         os.remove("./new_img_license/new_image" +str(count)+ ".png")
                    
            # print(detect[n_detect - 1].shape)
            # cv.imshow("Video", frame)
            
    else:
        break
A = []
for i in range(len(same_detect) - 1):
    for j in range(len(same_detect)):
        if(np.isclose(same_detect[i].shape, same_detect[j].shape, rtol=10, atol=10).all()):
            if(A != same_detect[i].all()):
                count+=1
                A.append(same_detect[i].all())
                cv.imwrite("./new_img_license/new_image" +str(count)+ ".png", new_img)
    pass
end_time = time.time() - start_time
print("Time to run code is: " + str(end_time))
cap.release()
video_save.release()
cv.destroyAllWindows()

# import numpy as np
# tuple1 = (1, 2, 3)
# tuple2 = (2, 3, 3)
# if np.isclose(tuple1, tuple2, rtol=5, atol=5).all():
#     print("Hai tuple gần bằng nhau")
# else:
#     print("Hai tuple khác nhau")
# print(tuple1 < tuple2)
