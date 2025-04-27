from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.colorpicker import ColorPicker
from kivy.graphics import Color, RoundedRectangle
from ui.components import RoundedButton

class EditScreen(Screen):
    def __init__(self, user, **kwargs):
        super(EditScreen, self).__init__(**kwargs)
        self.user = user

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        topBar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        # titolo
        title = Label(
            text="Edit Device",
            font_size=28,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(1, 1),
            color=(1, 1, 1, 1)
        )
        title.bind(size=title.setter('text_size'))

        topBar.add_widget(title)
        self.layout.add_widget(topBar)

        #Rounded input field function
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
        self.layout.add_widget(Label(text="Name", color=(1, 1, 1, 1)))
        nameContainer, self.nameInput = createRoundedInput("Enter name")
        self.layout.add_widget(nameContainer)

        # ID Input (non modificabile)
        self.layout.add_widget(Label(text="ID", color=(1, 1, 1, 1)))
        idContainer, self.idInput = createRoundedInput("Device ID")
        self.idInput.disabled = True  # ID non modificabile
        self.layout.add_widget(idContainer)

        # Color Picker
        self.layout.add_widget(Label(text="Color", color=(1, 1, 1, 1)))
        self.colorPicker = ColorPicker(size_hint=(1, None), height=300)
        self.layout.add_widget(self.colorPicker)

        # Save Button
        saveButton = RoundedButton(
            text="Save Changes",
            background_color=(0.2, 0.6, 0.9, 1),
            size_hint_y=None,
            height=40
        )
        saveButton.bind(on_release=self.onSave)

        self.layout.add_widget(saveButton)
        self.add_widget(self.layout)

    def onEnter(self):
        editId = self.user.editId

        # Cerca il device da modificare
        for device in self.user.devices:
            if device["id"] == editId:
                self.nameInput.text = device["name"]
                self.idInput.text = device["id"]
                self.colorPicker.color = device["color"]
                break

    def onSave(self, instance):
        deviceName = self.nameInput.text.strip()
        deviceId = self.idInput.text.strip()
        color = self.colorPicker.color

        if not deviceName:
            return

        # Trova e aggiorna il device
        for device in self.user.devices:
            if device["id"] == deviceId:
                device["name"] = deviceName
                device["color"] = color.copy()
                print(f"Device '{deviceName}' updated successfully.")
                break
        
        self.user.jsonSave()
