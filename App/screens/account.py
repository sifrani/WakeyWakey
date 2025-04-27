from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle
from ui.components import RoundedButton

class AccountScreen(Screen):
    def __init__(self, user, **kwargs):
        super(AccountScreen, self).__init__(**kwargs)
        self.user = user  # salvo l'oggetto user

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Title
        title = Label(
            text="Host",
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

        # Funzione per creare input tondi
        def create_rounded_input(hint, text=""):
            container = FloatLayout(size_hint_y=None, height=40)
            with container.canvas.before:
                Color(0.15, 0.15, 0.15, 1)
                bg = RoundedRectangle(pos=container.pos, size=container.size, radius=[10])
            def update_bg(*args):
                bg.pos = container.pos
                bg.size = container.size
            container.bind(pos=update_bg, size=update_bg)

            input_field = TextInput(
                hint_text=hint,
                text=text,  # <-- testo iniziale
                size_hint=(1, 1),
                pos_hint={"center_y": 0.5},
                background_color=(0, 0, 0, 0),
                foreground_color=(1, 1, 1, 1),
                cursor_color=(1, 1, 1, 1),
                hint_text_color=(0.6, 0.6, 0.6, 1),
                multiline=False,
                padding=(20, 10)
            )
            container.add_widget(input_field)
            return container, input_field

        # Input host
        layout.add_widget(Label(text="Host name", color=(1, 1, 1, 1)))
        name_container, self.name_input = create_rounded_input("Enter host", text=self.user.host)
        layout.add_widget(name_container)

        # Input port
        layout.add_widget(Label(text="Port", color=(1, 1, 1, 1)))
        port_container, self.port_input = create_rounded_input("Enter port", text=self.user.port)
        layout.add_widget(port_container)

        # Bottone save
        submit_button = RoundedButton(
            text="Save",
            background_color=(0.2, 0.6, 0.9, 1),
            size_hint_y=None,
            height=40
        )
        submit_button.bind(on_press=self.save_user_data)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def save_user_data(self, instance):
        self.user.host = self.name_input.text
        self.user.port = self.port_input.text
        self.user.startSocket()
        print("dioave")
        self.user.jsonSave()
