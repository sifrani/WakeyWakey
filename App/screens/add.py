from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker
from kivy.graphics import Color, RoundedRectangle
from ui.components import RoundedButton 
from kivy.uix.button import Button

class AddScreen(Screen):
    def __init__(self, user, **kwargs):
        super(AddScreen, self).__init__(**kwargs)
        self.user = user

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        topBar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # Title (left-aligned)
        title = Label(
            text="Add Device",
            font_size=28,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(1, 1),
            color=(1, 1, 1, 1)
        )
        title.bind(size=title.setter('text_size'))

        topBar.add_widget(title)
        layout.add_widget(topBar)

        # Rounded input field function
        def createRoundedInput(hint):
            container = FloatLayout(size_hint_y=None, height=40)
            with container.canvas.before:
                Color(0.15, 0.15, 0.15, 1)
                bg = RoundedRectangle(pos=container.pos, size=container.size, radius=[10])
            def updateBg(*args):
                bg.pos = container.pos
                bg.size = container.size
            container.bind(pos=updateBg, size=updateBg)

            inputField = TextInput(
                hint_text=hint,
                size_hint=(1, 1),
                pos_hint={"center_y": 0.5},
                background_color=(0, 0, 0, 0),
                foreground_color=(1, 1, 1, 1),
                cursor_color=(1, 1, 1, 1),
                hint_text_color=(0.6, 0.6, 0.6, 1),
                multiline=False,
                padding=(20, 10)
            )
            container.add_widget(inputField)
            return container, inputField

        # Name Input
        layout.add_widget(Label(text="Name", color=(1, 1, 1, 1)))
        nameContainer, self.nameInput = createRoundedInput("Enter name")
        layout.add_widget(nameContainer)

        # ID Input
        layout.add_widget(Label(text="ID", color=(1, 1, 1, 1)))
        idContainer, self.idInput = createRoundedInput("Enter MAC")
        layout.add_widget(idContainer)

        # Color Picker
        layout.add_widget(Label(text="Color", color=(1, 1, 1, 1)))
        self.colorPicker = ColorPicker(size_hint=(1, None), height=300)
        layout.add_widget(self.colorPicker)

        # Submit Button
        submitButton = RoundedButton(
            text="Add Device",
            background_color=(0.2, 0.6, 0.9, 1),
            size_hint_y=None,
            height=40
        )
        submitButton.bind(on_release=self.onSubmit)

        layout.add_widget(submitButton)
        self.add_widget(layout)

    def onSubmit(self, instance):
        deviceName = self.nameInput.text
        deviceId = self.idInput.text
        color = self.colorPicker.color  # Ottieni il colore scelto

        self.addDevice(deviceName, deviceId, color)

    def addDevice(self, deviceName, deviceId, color=(0.1, 0.4, 0.7, 1)):
        # Puliamo gli input
        deviceName = deviceName.strip()
        deviceId = deviceId.strip()

        # Controllo campi vuoti
        if not deviceName or not deviceId:
            print("Error: Name and Device ID must be filled.")
            return

        # Controllo duplicati sull'ID
        for device in self.user.devices:
            if device["id"].lower() == deviceId.lower():
                print("Error: Device with this ID already exists.")
                return

        # Aggiungo il nuovo device
        newDevice = {
            "name": deviceName,
            "id": deviceId,
            "color": color.copy()
        }
        self.user.devices.append(newDevice)
        self.user.jsonSave()

        print(f"Device '{deviceName}' added successfully.")
