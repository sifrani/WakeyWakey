from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle


class InfoScreen(Screen):
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        box = BoxLayout(orientation='vertical', padding=20)
        label = Label(text="Info Page", font_size=28, color=(1, 1, 1, 1))
        box.add_widget(label)
        self.add_widget(box)

