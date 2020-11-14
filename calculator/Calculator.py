from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
from kivy.uix.image import Image
from kivy.lang import Builder
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

Builder.load_string("""
<ScreenManagement>:
    id: screen_manager
    MainScreen:
        id: main_screen
        name: 'osd_screen'
    PauseScreen:
        id: pause_screen
        name: 'pause'

<MainScreen>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        Image:
            source: "./Images/Logo.png"
            center_x: self.parent.center_x
            center_y: self.parent.center_y

            

<PauseScreen>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Welcome to Bajil Bois Association'
            font_size: 25
""")
class PauseScreen(Screen):

    def on_enter(self):
        print('enter')
        #Clock.schedule_once(self.switch_back, 5)

    # def switch_back(self, *args):
    #     print('back')
    #     self.manager.current = "osd_screen"


class MainScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(self.switch, 5)

    def switch(self, *args):
        self.manager.current = "pause"


class ScreenManagement(ScreenManager):
    stop = threading.Event()


class OsdApp(App):
    def on_stop(self):
        self.root.stop.set()

    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    OsdApp().run()
    # class MainApp(App):
    #     def build(self):
    #         Window.clearcolor = (1, 1, 1, 1)
    #         img = Image(source='./Images/Logo.png',size_hint=(1, .5),pos_hint={'center_x':.5, 'center_y':.5})
    #         return img


    # if __name__ == '__main__':
    #     app = MainApp()
    #     app.run()