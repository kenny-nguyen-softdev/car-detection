import cv2 as cv
from ultralytics import YOLO
import time
from time import sleep
import numpy as np
from tracker import *
import pytesseract


class ModuleOfCar:
    detect_license = []
    n_detect_license = 0
    def detection_car(self, file_path):
        model = YOLO('yolov8n.pt')
        video_path = file_path
        cap = cv.VideoCapture(video_path)
        width_video = int(cap.get(3))
        height_video = int(cap.get(4))
        size_of_video = (width_video, height_video)
        video_save = cv.VideoWriter(
            "./Videos/video_detect_car.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                results = model(frame)
                annotated_frame = results[0].plot()
                video_save.write(annotated_frame)
                if cv.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        video_save.release()
        cv.destroyAllWindows()
        pass

    def pega_centro(self, x, y, w, h):
        x1 = int(w / 2)
        y1 = int(h / 2)
        cx = x + x1
        cy = y + y1
        return cx, cy

    def vehicle_couting_car(self, file_path):
        model = YOLO('yolov8n.pt')
        video_path = file_path
        cap=cv.VideoCapture(video_path)

        count=0
        tracker = Tracker()

        area1 = [(387,479),(382,447),(480,438),(494,479)]
        area_1 = set()
        size_of_video = (1020,600)
        video_save = cv.VideoWriter(
             "./Videos/video_counting.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
        while True:
            ret,frame=cap.read()
            if not ret:
                break
            count += 1
            if count % 3 != 0:
                continue
            frame=cv.resize(frame,(1020,600))
            results=model(frame)
            list = []
            for r in results[0].boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = r
                x1 = int(x1)
                y1 = int(y1)
                x2 = int(x2)
                y2 = int(y2)  
                # cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                list.append([x1,y1,x2,y2])
            idx_bbox = tracker.update(list)
            for bbox in idx_bbox:
                x3,y3,x4,y4,id = bbox
                cv.rectangle(frame,(x3,y3),(x4,y4),(0,0,255),2)
                # cx,cy = pega_centro(x3,y3,x4,y4)
                cv.circle(frame,(x4,y4),4,(0,255,0),-1)
                result = cv.pointPolygonTest(np.array(area1,np.int32),((x4,y4)),False)
                if result > 0:
                    area_1.add(id)
            cv.polylines(frame,[np.array(area1,np.int32)], True,(0,255,255),2)
            a1 =len(area_1)
            cv.putText(frame,"___HCMUTE___",(40,46),cv.FONT_HERSHEY_TRIPLEX,2,(144, 43, 43),2,cv.LINE_AA)
            cv.putText(frame,"So luong xe di qua la :" + str(a1),(44,105),cv.FONT_HERSHEY_TRIPLEX,2,(144,43,43),2,cv.LINE_AA)
            # cv.imshow("FRAME",frame)
            video_save.write(frame)
            if cv.waitKey(0)&0xFF==27:
                break
        cap.release()
        cv.destroyAllWindows()
    def detect_license_car(self,file_path):
        model = YOLO('model_bien_so.pt')
        video_path = file_path
        cap = cv.VideoCapture(video_path)
        width_video = int(cap.get(3))
        height_video = int(cap.get(4))
        size_of_video = (width_video, height_video)
        video_save = cv.VideoWriter(
            "./Videos/video_licence_car.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
        count = 0
        start_time = time.time()
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                results = model(frame)
                annotated_frame = results[0].plot()
                video_save.write(annotated_frame)
                for r in results[0].boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = r
                    x1 = int(x1)
                    y1 = int(y1)
                    x2 = int(x2)
                    y2 = int(y2)
                    image_car = np.array(results[0].orig_img)
                    # Tu anh goc cat anh co chua bien so co toa do (x1:x2,y1:y2)
                    new_img = image_car[y1:y2, x1:x2]
                    self.detect_license.append(new_img)
                    self.n_detect_license +=1
                    if(len(self.detect_license) == 1 or (self.detect_license[self.n_detect_license - 1].all() != self.detect_license[self.n_detect_license -2].all())):
                        count += 1
                        cv.imwrite("./new_img_license/new_image_license" + str(count) + ".png", new_img)
            else:
                break
        end_time = time.time() - start_time
        print("Time to run code is: " + str(end_time))
        cap.release()
        video_save.release()
        cv.destroyAllWindows()
        pass
    def convert_to_text(self,file_path,count):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
        img = cv.imread(file_path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
        cv.imwrite("./New_img_convert/new_image_convert" + str(count) + ".png", thresh)
        text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
        return text
        pass
