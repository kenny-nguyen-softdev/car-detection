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
import module
import time

LabelBase.register(
    name="font2", fn_regular="D:\Hk2_Nam3\Image_Processing\Final_Project\Font\\font2.ttf")


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
    i = 0
    file_path_video = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    detect_car = module.ModuleOfCar()

    def __init__(self, **kwargs):
        super(TheThirdScreen, self).__init__(**kwargs)

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

    def detect_object(self):
        start_time = time.time()
        self.detect_car.detection_car(self.file_path_video)
        self.end_time = time.time() - start_time
        self.ids.video3.source = "./Videos/video4.avi"
        print(self.end_time)

    def cancel(self):
        self.the_popup.dismiss()

    def play_video(self):
        self.ids.video3.state = "play"
        print(self.ids.video3.state)

    def on_start(self):
        Clock.schedule_interval(self.update_label, 0.5)

    def update_label(self, *args):
        self.times += 1
        new_time = self.ids.time.text.replace(str(self.i), str(self.times))
        self.ids.time.text = new_time
        self.i += 1

    def pause_video(self):
        self.ids.video3.state = "pause"
        print(self.ids.video3.state)
    pass


class TheFourthScreen(Screen):
    pass


kv = Builder.load_file("my.kv")


class MyApp(App):

    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()
