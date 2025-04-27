from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from screens.account import AccountScreen
from screens.add import AddScreen
from screens.devices import DevicesScreen
from screens.info import InfoScreen
from screens.options import OptionsScreen
from screens.edit import EditScreen
from ui.components import BottomNavBar
from kivy.core.window import Window

import socket, json

class User():
    def __init__(self):
        self.devices = [
            {"name": "Raspberry", "id": "ssh.org", "color": (0.1, 0.4, 0.7, 1)},
        ]
        self.host = ""  
        self.port = "" 
        self.conn = None
        self.sock = None
        self.editId = None
        self.editScreen = None
        self.sm = None
        self.n, self.e = None, None
        self.jsonLoad()

        self.startSocket()

    def jsonLoad(self):
        with open('memory.json') as f:
            data = json.load(f)
            self.devices = data["devices"]
            self.host = data["host"]
            self.port = data["port"]

    def jsonSave(self):
        data = {
            "devices": self.devices,
            "host": self.host,
            "port": self.port
        }
        jsonObj = json.dumps(data, indent=4)
        with open("memory.json", "w") as file:
            file.write(jsonObj)

    def startSocket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, int(self.port)))
            self.sock.listen()
            self.conn, addr = self.sock.accept()
            self.n, self.e = self.getPublicKey()
        except:
            pass#per scelta del proggetista legata alla sicurezza non c'e' modo di sapere se le richieste sono andate a buon fine

    def closeSocket(self):
        try:
            if self.conn:
                self.conn.sendall(b"close")
                self.conn.close()
            if self.sock:
                self.sock.close()
        except:
            pass

    def getPublicKey(self):
        try:
            if self.conn:
                self.conn.sendall(b"publicKey")
                data = b""
                while True:
                    part = self.conn.recv(4096)
                    if not part:
                        break
                    data += part
                    if b"public exponent:" in part:
                        break
                response = data.decode()
                lines = response.splitlines()
                modulus = ""
                for i, line in enumerate(lines):
                    if "modulus:" in line:
                        modulus = "".join(lines[i+1:i+12]).replace(" ", "").replace("\n", "")
                    if "public exponent:" in line:
                        exponent = int(line.split(":")[1].strip())
                n = int(modulus)
                e = exponent
                return n, e
            else:
                return None, None
        except:
            return None, None

    def on(self, macAddress):
        try:
            encrypted_mac = self.cryptRSA(macAddress, self.n, self.e)
            message = f"on {encrypted_mac}".encode()
            self.conn.sendall(message)
        except:
            pass

    @staticmethod
    def cryptRSA(text, n, e):
        def textToBinary(text):
            n = 0
            for c in text:
                n += ord(c)
                n <<= 8
            n >>= 8
            return n

        def binaryToText(n):
            bytesN = []
            while n != 0:
                bytesN.append(n % 256)
                n >>= 8
            text = ""
            for byte in reversed(bytesN):
                text += chr(byte)
            return text

        l = 0
        n_ = n
        while n_ >= 256:
            n_ >>= 8
            l += 1

        binaryStrings = [textToBinary(text[i:i+l]) for i in range(0, len(text), l)]
        encrypted = [(x**e) % n for x in binaryStrings]
        result = ""
        for number in encrypted:
            result += binaryToText(number)
        return result


        

class ClientApp(App):
    def build(self):
        Window.size = (400, 840)
        Window.clearcolor = (0.07, 0.07, 0.07, 1)
        main_layout = BoxLayout(orientation='vertical')
        self.sm = ScreenManager(transition=FadeTransition())
        user.sm = self.sm

        self.sm.add_widget(DevicesScreen(user, name="devices"))
        self.sm.add_widget(AccountScreen(user, name="account"))
        self.sm.add_widget(AddScreen(user, name="add"))
        self.sm.add_widget(InfoScreen(name="info"))
        self.sm.add_widget(OptionsScreen(name="options"))
        es = EditScreen(user,name="edit")
        self.sm.add_widget(es)
        user.es = es
        main_layout.add_widget(self.sm)
        main_layout.add_widget(BottomNavBar(self.sm))
        return main_layout

user:User = None

if __name__ == '__main__':
    user = User()
    sa = ClientApp().run()