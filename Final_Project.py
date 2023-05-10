from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2 as cv
import os
import module
from ultralytics import YOLO
import time
from threading import Thread
import threading

LabelBase.register(
    name="font2", fn_regular="./Font/font2.ttf")


class WindowLoading(Popup):
    pass


class Content_Loading(FloatLayout):
    pass


class WindowExit(Popup):
    pass


class WindowLoadVideo(Popup):
    pass


class Content(FloatLayout):
    load = ObjectProperty()
    cancel = ObjectProperty()
    pass


class MainWindow(ScreenManager):
    pass


class NotificationExitApp(FloatLayout):
    cancel = ObjectProperty()


class TheFirstScreen(Screen):
    the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = WindowExit()
        content_exit = NotificationExitApp(cancel=self.cancel)
        self.the_popup.add_widget(content_exit)
        self.the_popup.open()

    def cancel(self):
        self.the_popup.dismiss()
    pass


class TheSecondScreen(Screen):
    pass


class TheThirdScreen(Screen):
    times = 0
    end_time = 0
    current = None
    i = 0
    file_path_video = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    detect_car = module.ModuleOfCar()
    the_popup_loading = ObjectProperty(None)
    texture = Texture.create(size=(200, 100))

    def __init__(self, **kwargs):
        super(TheThirdScreen, self).__init__(**kwargs)

    def Reset(self):
        DirPath = ".\Videos"
        Files = os.listdir(DirPath)
        for File in Files:
            if (File == 'video4.avi'):
                os.remove(File)
                break
            else:
                break
        pass

    def open_popup_loading(self):
        self.the_popup_loading = WindowLoading()
        contentloading = Content_Loading()
        self.the_popup_loading.add_widget(contentloading)
        self.the_popup_loading.open()

    def open_popup(self):
        self.the_popup = WindowLoadVideo()
        content = Content(load=self.load, cancel=self.cancel)
        self.the_popup.add_widget(content)
        self.the_popup.open()

    def load(self, selection):
        self.file_path_video = str(selection[0])
        self.the_popup.dismiss()
        try:
            self.ids.video3.source = self.file_path_video
            print("File name " + self.ids.video3.source)
        except:
            pass

    def cancel(self):
        self.the_popup.dismiss()

    def detect_object(self):
        start_time = time.time()
        # self.on_start()
        self.clock_show_video = Clock.schedule_once(self.show_video, 2)
        self.end_time = time.time() - start_time
        print("Time to solve video is: " + str(self.end_time) + "s")

    def show_video(self, *args):
        # t = threading.Thread(
        #     self.detection_car(self.file_path_video))
        # t.start()
        self.ids.video3.source = "./runs/detect/predict2/video70.mp4"
        # self.the_popup_loading.dismiss()
        self.clock_show_video.cancel()

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
                self.texture.blit_buffer(
                    annotated_frame.tobytes(), colorfmt='rgb')
                self.ids.video3.texture = self.texture
                # video_save.write(annotated_frame)
                if cv.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        video_save.release()
        cv.destroyAllWindows()

    def play_video(self):
        self.ids.video3.state = "play"
        print(self.ids.video3.state)

    def print_number(self):
        for i in range(0, 10):
            print("Number is : " + str(i))
            time.sleep(1)

    def pause_video(self):
        self.ids.video3.state = "pause"
        print(self.ids.video3.state)
    pass

    def couting_car(self):
        start_time = time.time()
        self.detect_car.vehicle_couting_car(self.file_path_video)
        self.end_time = time.time() - start_time
        self.ids.video3.source = "./Videos/video10.avi"
        print("End time to slove" + str(self.end_time))
        pass

    def on_start(self):
        self.function_clock = Clock.schedule_interval(self.press_it, 1)
        pass

    def stop_function(self, *args):
        self.function_clock.cancel()

    def press_it(self, *args):
        self.current = self.ids.my_progress_bar.value
        if (self.current == 100):
            self.current = 0
            self.ids.my_progress_bar.value = self.current
        self.current += 10
        self.ids.my_progress_bar.value = self.current
        self.ids.load.text = "LOADING"


class TheFourthScreen(Screen):
    pass


kv = Builder.load_file("my.kv")


class MyApp(App):

    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()
