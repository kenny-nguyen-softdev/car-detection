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

LabelBase.register(
    name="font2", fn_regular="D:\Hk2_Nam3\Image_Processing\Final_Project\Font\\font2.ttf")


class WindowExit(Popup):
    pass


class MainWindow(ScreenManager):
    pass


class NotificationExitApp(FloatLayout):

    def exit_app(self):
        App.get_running_app().stop()
        Window.close()
    pass

    def cancel_popup(self):
        self.the_popup_exit = TheFirstScreen()
        self.the_popup_exit.cancel_popup()
    pass


class TheFirstScreen(Screen):
    the_popup = ObjectProperty(None)

    def open_popup(self):
        self.the_popup = WindowExit()
        content_exit = NotificationExitApp()
        self.the_popup.add_widget(content_exit)
        self.the_popup.open()

    def cancel_popup(self):
        print("cancel")
        WindowExit().dismiss()
    pass


class TheSecondScreen(Screen):
    pass


class TheThirdScreen(Screen):

    def __init__(self, **kwargs):
        super(TheThirdScreen, self).__init__(**kwargs)

    def play_video(self):
        self.ids.video3.state = "play"
        print(self.ids.video3.state)

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
