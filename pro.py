import cv2 as cv
from ultralytics import YOLO
import time
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.graphics import Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.clock import Clock
# model = YOLO('yolov8n.pt')
# start_time = time.time()
# model.predict(source="./Videos/video2.mp4", show=True, save=True, show_labels=False, show_conf=False,
#               conf=0.5, save_txt=False, save_crop=False, line_thickness=2, box=True, visualize=False)
# end_time = time.time() - start_time
# print("Time to slove is : " + str(end_time))

# model = YOLO('yolov8n.pt')
# video_path = './Videos/video2.mp4'
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
#         cv.imshow("Video", annotated_frame)
#         # video_save.write(annotated_frame)
#         if cv.waitKey(10) & 0xFF == ord('q'):
#             break
#     else:
#         break
# cap.release()
# video_save.release()


class MyLayOut(BoxLayout):

    # def __init__(self, **kwargs):
    #     super(MyLayOut).__init__(**kwargs)
    tex = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyLayOut, self).__init__(**kwargs)
        Clock.schedule_once(self.texture_init, 0)

    def texture_init(self, instance):
        self.tex = Texture.create(size=(600, 400))

    def show_video(self):
        cap = cv.VideoCapture('./Videos/video2.mp4')
        ret, frame = cap.read()
        while (ret):
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(
                frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.ids.video3.texture = self.tex
            cv.waitKey(30)
            ret, frame = cap.read()
        cap.release()
        cv.destroyAllWindows()

    # def load_video(self):
    #     self.video_player = self.ids.video
    #     self.video_player.texture = Texture.create(size=(640, 480))
    #     self.video_player.texture_size = self.video_player.texture.size

    # def update(self, dt):
    #     ret, frame = self.video_capture.read()
    #     if ret:
    #         frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    #         texture = Texture.create(
    #             size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
    #         texture.blit_buffer(
    #             frame.tostring(), colorfmt='rgb', bufferfmt='ubyte')
    #         self.video_player.texture = texture
    pass


class ProApp(App):
    def build(self):
        return MyLayOut()


if __name__ == '__main__':
    ProApp().run()
