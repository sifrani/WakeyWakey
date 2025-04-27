from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Title (left-aligned)
        title = Label(
            text="Options",
            font_size=28,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(1, 1),
            color=(1, 1, 1, 1)
        )
        title.bind(size=title.setter('text_size'))

        top_bar.add_widget(title)

        layout.add_widget(top_bar)

        self.add_widget(layout)
