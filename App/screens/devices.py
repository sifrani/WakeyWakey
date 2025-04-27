from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from ui.components import Card
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, RoundedRectangle

class DevicesScreen(Screen):
    def __init__(self, user, **kwargs):
        super().__init__(**kwargs)
        self.user = user
        self.filteredDevices = user.devices

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        topBar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        title = Label(
            text="Devices",
            font_size=28,
            bold=True,
            halign="left",
            valign="middle",
            size_hint=(1, 1),
            color=(1, 1, 1, 1)
        )
        title.bind(size=title.setter('text_size'))

        reloadBtn = Image(
            source="icons/reload.png",
            size_hint=(None, None),
            size=(24, 24)
            
        )

        topBar.add_widget(title)
        topBar.add_widget(reloadBtn)

        self.layout.add_widget(topBar)

        # Search bar
        searchLayout = FloatLayout(size_hint_y=None, height=40)
        with searchLayout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.searchBg = RoundedRectangle(pos=searchLayout.pos, size=searchLayout.size, radius=[20])
        def updateSearchBg(*args):
            self.searchBg.pos = searchLayout.pos
            self.searchBg.size = searchLayout.size
        searchLayout.bind(pos=updateSearchBg, size=updateSearchBg)

        self.searchInput = TextInput(
            hint_text="Search",
            size_hint=(1, 1),
            pos_hint={"center_y": 0.5},
            padding=(40, 10),
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            hint_text_color=(0.6, 0.6, 0.6, 1),
            multiline=False
        )
        self.searchInput.bind(text=self.onSearchText)

        searchIcon = Image(
            source="icons/search.png",
            size_hint=(None, None),
            size=(20, 20),
            pos_hint={"center_y": 0.5, "x": 0.02}
        )

        searchLayout.add_widget(self.searchInput)
        searchLayout.add_widget(searchIcon)
        self.layout.add_widget(searchLayout)

        self.scroll = ScrollView()
        self.servers = GridLayout(cols=1, spacing=20, size_hint_y=None)
        self.servers.bind(minimum_height=self.servers.setter('height'))

        self.scroll.add_widget(self.servers)
        self.layout.add_widget(self.scroll)

        self.add_widget(self.layout)

        self.updateDevices()

    def onSearchText(self, instance, value):
        searchText = value.lower()
        self.filteredDevices = [
            device for device in self.user.devices
            if searchText in device["name"].lower() or searchText in device["id"].lower()
        ]
        self.updateDevices()

    def updateDevices(self):
        self.servers.clear_widgets()
        for device in self.filteredDevices:
            self.servers.add_widget(Card(self.user, device["name"], device["id"], "search.png", device["color"]))
