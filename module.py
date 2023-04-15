import cv2 as cv
from ultralytics import YOLO
import time
from time import sleep
import numpy as np


class ModuleOfCar:
    largura_min = 80  # Largura minima do retangulo
    altura_min = 80  # Altura minima do retangulo

    offset = 6  # Erro permitido entre pixel

    pos_linha = 550  # Posição da linha de contagem

    delay = 60  # FPS do vídeo

    detec = []
    carros = 0

    def detection_car(self, file_path):
        model = YOLO('yolov8n.pt')
        video_path = file_path
        cap = cv.VideoCapture(video_path)
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
        cap = cv.VideoCapture(file_path)
        width_video = int(cap.get(3))
        height_video = int(cap.get(4))
        size_of_video = (width_video, height_video)
        video_save = cv.VideoWriter(
            "./Videos/video10.avi", cv.VideoWriter_fourcc(*'MJPG'), 10, size_of_video)
        subtracao = cv.createBackgroundSubtractorMOG2()

        while True:
            ret, frame1 = cap.read()
            tempo = float(1/self.delay)
            sleep(tempo)
            grey = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(grey, (3, 3), 5)
            img_sub = subtracao.apply(blur)
            dilat = cv.dilate(img_sub, np.ones((5, 5)))
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
            dilatada = cv.morphologyEx(dilat, cv. MORPH_CLOSE, kernel)
            dilatada = cv.morphologyEx(dilatada, cv. MORPH_CLOSE, kernel)
            contorno, h = cv.findContours(
                dilatada, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

            cv.line(frame1, (25, self.pos_linha),
                    (1200, self.pos_linha), (255, 127, 0), 3)
            for (ica, c) in enumerate(contorno):
                (x, y, w, h) = cv.boundingRect(c)
                validar_contorno = (w >= self.largura_min) and (
                    h >= self.altura_min)
                if not validar_contorno:
                    continue
                cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                centro = self.pega_centro(x, y, w, h)
                self.detec.append(centro)
                cv.circle(frame1, centro, 4, (0, 0, 255), -1)
                for (x, y) in self.detec:
                    if y < (self.pos_linha+self.offset) and y > (self.pos_linha-self.offset):
                        self.carros += 1
                        cv.line(frame1, (25, self.pos_linha),
                                (1200, self.pos_linha), (0, 127, 255), 3)
                        self.detec.remove((x, y))
                        print("car is detected : "+str(self.carros))

            cv.putText(frame1, "VEHICLE COUNT : "+str(self.carros), (450, 70),
                       cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
            # cv.imshow("Video Original", frame1)
            # cv.imshow("Detectar", dilatada)
            video_save.write(frame1)

            if cv.waitKey(1) == 27:
                break

        cap.release()
        video_save.release()
        cv.destroyAllWindows()
