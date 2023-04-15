import cv2 as cv
import cv2
from ultralytics import YOLO
import time

class ModuleOfCar:
    def detection_car(self, file_path):
        model = YOLO('yolov8n.pt')
        video_path = file_path
        cap = cv2.VideoCapture(video_path)
        width_video = int(cap.get(3))
        height_video = int(cap.get(4))
        size_of_video = (width_video, height_video)
        video_save = cv.VideoWriter(
            "./Videos/video4.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
        while cap.isOpened():
            success, frame = cap.read()

            if success:
                results = model(frame)

                annotated_frame = results[0].plot()

                video_save.write(annotated_frame)

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        video_save.release()
        cv2.destroyAllWindows()
        pass
