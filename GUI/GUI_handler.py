from util.UtilConstants import UtilConstants
import data_base_lib
from Constants import ClientConstants
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from Constants import Images

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput


from GUI.AdvancedButton import AdvancedButton

path = UtilConstants.DATA_BASES_PATH
table = data_base_lib.default()

'''
    Screens
'''


class ScreenManagement(ScreenManager):
    pass


class MainScreen(Screen):
    pass


class AttacksLogScreen(Screen):
    pass

'''
    Widgets & Utils
'''


class ImageButton(AdvancedButton, Image):
    pass


class TextButton(AdvancedButton, Label):
    pass


class BackButton(TextButton):
    pass


class TransTextInput(TextInput):
    def __init__(self, **kwargs):
        super(TransTextInput, self).__init__(**kwargs)


class AttackLabel(ButtonBehavior, Label):
    def __init__(self, attack_info: list, **kwargs, ):
        super().__init__(**kwargs)
        self.attack_info = attack_info
        self.opacity = 1

    def on_press(self):
        self.opacity = 0.5

    def on_release(self):
        self.opacity = 1


class AttacksLog(ScrollView):
    def __init__(self, **kwargs):
        super(AttacksLog, self).__init__(**kwargs)
        self.bar_width = 20
        self.pos = (243, 44)
        self.size_hint = (0.6, 0.57)
        self.scroll_type = ['bars']
        self.bar_inactive_color = (5, 20, 10, 0.5)
        self.do_scroll_x = False
        self.do_scroll_y = True
        self.__init__grid()

    def __init__grid(self):
        self.grid = GridLayout()
        self.grid.size_hint_y = None
        self.grid.cols = 1
        self.grid.spacing = 3
        self.grid.padding = (5, 0, 0, 0)
        self.grid.size_hint_x = 1.0
        # self.grid.row_default_height = '24dp'
        self.add_widget(self.grid)
        self.attack_list = []

    def add_attack(self, attack: list):
        text = ''
        print(attack)
        for i in attack:
            text += i + ' '

        label_to_add = AttackLabel(attack, text=text, color=[0, 0, 0, 1])
        # label_to_add.size_hint_y = None
        label_to_add.font_size = 30
        label_to_add.padding = (0, 0)
        label_to_add.height = len(self.attack_list) * 5
        label_to_add.valign = 'middle'
        label_to_add.halign = 'left'
        # increment grid height
        self.grid.height += label_to_add.height
        self.grid.add_widget(label_to_add)

        self.attack_list.append(attack)

    def update_attack_list(self):
        attack_list = ClientConstants.ATTACKS_DATA.select_all()
        print(attack_list)
        print('Here!!!!!!!!!!!!!!!!!!!!!!!!!!')
        for i in attack_list:
            self.add_attack(i)

    def clean(self):
        self.remove_widget(self.grid)
        self.__init__grid()

'''
    App
'''


class ClientGUI(App):
    def __init__(self, **kwargs):
        super(ClientGUI, self).__init__(**kwargs)
        self.assets = Images()
        self.kv_des = Builder.load_file(self.assets.KV_FILE)

        self.is_init = True
        Clock.schedule_interval(self.look_for_update, 2)

    def build(self):
        self.title = "System View"

        Window.size = (1200, 700)
        Window.fullscreen = False

        return self.kv_des

    def look_for_update(self, *args):
        if self.is_init:
            print('upadate!!!!!!!!!!!!!!!!!!!!!!!!!')
            self.root.ids.AttacksLogScreen.ids.AttacksLog.update_attack_list()
            self.is_init = False

        if ClientConstants.FOUND_ATTACK:
            attack = (ClientConstants.ATTACKS_DATA.select("attacker_mac", ClientConstants.ATTACKER_MAC_ADDRESS))[-1]
            self.root.ids.AttacksLogScreen.ids.AttacksLog.add_attack(attack)
            ClientConstants.FOUND_ATTACK = False


def main():
    app = ClientGUI()
    app.run()


if __name__ == '__main__':
    main()
