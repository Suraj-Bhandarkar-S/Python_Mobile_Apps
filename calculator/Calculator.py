from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager, Screen
import threading
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import math
Config.set('graphics', 'width', '500') 
Config.set('graphics', 'height', '400') 

Builder.load_string("""
<ScreenManagement>:
    id: screen_manager
    MainScreen:
        id: main_screen
        name: 'osd_screen'
    CalciScreen:
        id: calci_screen
        name: 'calci'


<ScaleLabel@Label>:
    _scale: 1. if self.texture_size[0] < self.width else float(self.width) / self.texture_size[0]
    canvas.before:
        PushMatrix
        Scale:
            origin: self.center
            x: self._scale or 1.
            y: self._scale or 1.
    canvas.after:
        PopMatrix
        
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
           
            font_size: 25
""")
red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]
import random
class CalciScreen(Screen):

    def on_enter(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None
        main_layout = BoxLayout(orientation="vertical")
        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=55
        )
        main_layout.add_widget(self.solution)
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
        ]
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        equals_button = Button(
            text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        self.add_widget(main_layout)

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        else:
            if current and (
                self.last_was_operator and button_text in self.operators):
                # Don't add two operators right after each other
                return
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
        self.last_button = button_text
        self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            solution = str(eval(self.solution.text))
            self.solution.text = solution
        


class MainScreen(Screen):

    def on_enter(self):
        Clock.schedule_once(self.switch, 5)

    def switch(self, *args):
        self.manager.current = "calci"


class ScreenManagement(ScreenManager):
    stop = threading.Event()


class CalculatorApp(App):
    def on_stop(self):
        self.root.stop.set()

    def build(self):
        return ScreenManagement()


if __name__ == '__main__':
    CalculatorApp().run()
