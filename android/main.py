from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.storage.dictstore import DictStore
import datetime
import socket
import atexit

class UI(BoxLayout):
    def __init__(self, **kwargs):
        super(UI, self).__init__(**kwargs)

        """
        Initial Configuration
        """
        #self.b_white = False
        #self.b_red = False
        #self.b_green = False
        #self.b_blue = False
        self.vl_white = 99
        self.vl_red = 99
        self.vl_green = 99
        self.vl_blue = 99
        self.progressive_light = False
        self.natural_light = False
        self.circadian_cycle = False
        now = datetime.datetime.now()

        """
        Creating Boxes for UI
        """
        box_left = BoxLayout(orientation = 'vertical')
        box_white = BoxLayout(orientation='vertical')
        box_red = BoxLayout(orientation='vertical')
        box_green = BoxLayout(orientation='vertical')
        box_blue = BoxLayout(orientation='vertical')
        box_preferences = BoxLayout(orientation='horizontal')

        """
        Creating Buttons for UI
        """

        self.save_button = Button(text='Save')
        self.load_button = Button(text='Load')

        self.natural_button = Button(text = 'Luz Natural', font_size=14)
        self.circadian_button = Button(text = 'Ciclo Circadiano', font_size=14)
        self.progressive_button = Button(text = 'Progressivo', font_size=14)

        self.clock_label = Label(text="Horario \n" + str(now.strftime("%H:%M:%S")))

        self.white_slider = Slider(min = 10, max = 99, value = 99, orientation = 'vertical', padding = 48)
        self.white_button = Button(text='Luz Branca', font_size=14)

        self.red_slider = Slider(min = 10, max = 99, value = 99, orientation = 'vertical', padding = 48)
        self.red_button = Button(text='Luz Vermelha', font_size=14)

        self.green_slider = Slider(min = 10, max = 99, value = 99, orientation = 'vertical', padding = 48)
        self.green_button = Button(text='Luz Verde', font_size=14)

        self.blue_button = Button(text='Luz Azul', font_size=14)
        self.blue_slider = Slider(min = 10, max = 99, value = 99, orientation = 'vertical', padding = 48)

        """
        Binding Buttons to Actions
        """

        self.white_button.bind(on_press=self.switch_white)
        self.red_button.bind(on_press=self.switch_red)
        self.green_button.bind(on_press=self.switch_green)
        self.blue_button.bind(on_press=self.switch_blue)

        self.white_slider.bind(value = self.white_slider_change)
        self.red_slider.bind(value = self.red_slider_change)
        self.green_slider.bind(value = self.green_slider_change)
        self.blue_slider.bind(value = self.blue_slider_change)

        self.save_button.bind(on_press=self.popup_save)
        self.load_button.bind(on_press=self.popup_load)

        self.natural_button.bind(on_press = self.switch_natural)
        self.circadian_button.bind(on_press=self.switch_circadiano)
        self.progressive_button.bind(on_press=self.switch_progressive)

        """
        Adding Widgets to Box
        """

        box_preferences.add_widget(self.save_button)
        box_preferences.add_widget(self.load_button)

        box_left.add_widget(box_preferences)
        box_left.add_widget(self.clock_label)
        box_left.add_widget(self.circadian_button)
        box_left.add_widget(self.natural_button)
        box_left.add_widget(self.progressive_button)

        box_white.add_widget(self.white_slider)
        box_white.add_widget(self.white_button)

        box_red.add_widget(self.red_slider)
        box_red.add_widget(self.red_button)

        box_green.add_widget(self.green_slider)
        box_green.add_widget(self.green_button)

        box_blue.add_widget(self.blue_slider)
        box_blue.add_widget(self.blue_button)

        """
        Adding Boxes to Application
        """
        self.add_widget(box_left)
        self.add_widget(box_white)
        self.add_widget(box_red)
        self.add_widget(box_green)
        self.add_widget(box_blue)

        """
        Scheduling to checkClock each second
        used in Circadian Cycle
        """
        Clock.schedule_interval(self.checkClock, 1)


    def send_message(self, message):

        for i in range(len(message)):
            print("Sending " + message[i])
            sock.sendall(message[i])

            amount_received = 0
            amount_expected = len(message[i])

            while amount_received < amount_expected:
                data = sock.recv(32)
                amount_received += len(data)
                print("Received " + str(data))

    def switch_circadiano(self, instance):
        self.natural_light = False
        self.circadian_cycle = True
        self.progressive_light = False

    def checkClock(self, *args):
        now = datetime.datetime.now()
        self.clock_label.text = "Horario \n" + str(now.strftime("%H:%M:%S"))
        if(self.circadian_cycle):
            # Change Light Status
            # 0 to 6 => Dim Light
            if (int(now.strftime("%H")) > 0 and int(now.strftime("%H")) < 6):
                message = "cw" + str(10)
                self.send_message(message)
            # 6 to 18 => Bright Light
            elif (int(now.strftime("%H")) > 6 and int(now.strftime("%H")) < 18):
                message = "cw" + str(99)
                self.send_message(message)
            # 0 to 6 => Dim Light
            elif (int(now.strftime("%H")) > 18 and int(now.strftime("%H")) < 24):
                message = "cw" + str(20)
                self.send_message(message)

    def switch_natural(self, instance):
        self.natural_light = True
        self.circadian_cycle = False
        self.progressive_light = False

        message = "un66"
        self.send_message(message)

    def switch_progressive(self, instace):
        self.natural_light = False
        self.circadian_cycle = False
        self.progressive_light = True

        message = "up99"
        self.send_message(message)

    def switch_white(self, instance):
        #self.b_white = True
        self.vl_white = str(self.vl_white)
        self.natural_light = False
        self.circadian_cycle = False
        self.progressive_light = False

        message = "cw" + str(self.vl_white)
        self.send_message(message)

    def switch_red(self, instance):
        #self.b_red = True
        self.vl_red = str(self.vl_red)
        self.natural_light = False
        self.circadian_cycle = False
        self.progressive_light = False

        message = "cr" + str(self.vl_red)
        self.send_message(message)

    def switch_green(self, instance):
        #self.b_green = True
        self.vl_green = str(self.vl_green)
        self.natural_light = False
        self.circadian_cycle = False
        self.progressive_light = False

        message = "cg" + str(self.vl_green)
        self.send_message(message)

    def switch_blue(self, instance):
        #self.b_blue = True
        self.vl_blue = str(self.vl_blue)
        self.natural_light = False
        self.circadian_cycle = False
        self.progressive_light = False

        message = "cb" + str(self.vl_blue)
        self.send_message(message)

    def white_slider_change(self, instance, value):
        if(not self.circadian_cycle):
            print("White changed to " + str(int(value)))
            self.vl_white = int(value)

    def red_slider_change(self, instance, value):
        if(not self.circadian_cycle):
            print("Red changed to " + str(int(value)))
            self.vl_red = int(value)

    def green_slider_change(self, instance, value):
        if(not self.circadian_cycle):
            print("Green changed to " + str(int(value)))
            self.vl_green = int(value)

    def blue_slider_change(self, instance, value):
        if(not self.circadian_cycle):
            print("Blue changed to " + str(int(value)))
            self.vl_blue = int(value)

    """
    Pop ups Methods
    """

    def popup_load(self, instance):

        def cancel(instance):
            popup.dismiss()

        def ok(instance):
            load_file = fileChooser.selection[0]
            print(str(load_file))
            with open(load_file, 'r') as stream:
                print(stream.read())

        fileChooser = FileChooserIconView(path="/home")

        popup_content = BoxLayout(orientation='vertical')
        buttons_box = BoxLayout(orientation='horizontal', size_hint = (0.3, 0.3))

        ok_button = Button(text="Ok", font_size = 14)
        cancel_button = Button(text="Cancel", font_size = 14)

        ok_button.bind(on_press = ok)
        cancel_button.bind(on_press = cancel)

        buttons_box.add_widget(ok_button)
        buttons_box.add_widget(cancel_button)
        popup_content.add_widget(fileChooser)
        popup_content.add_widget(buttons_box)

        popup = Popup(title="Load Preference", content= popup_content, size_hint = (0.5, 0.5))
        popup.open()

    def popup_save(self, instance):

        def cancel(instance):
            popup.dismiss()

        def ok(instance):
            file_name = str(text_input.text)

            current_config = {}

            current_config["file_name"] = file_name
            #current_config["b_white"] = self.b_white
            #current_config["b_red"] = self.b_red
            #current_config["b_green"] = self.b_green
            #current_config["b_blue"] = self.b_blue
            current_config["vl_white"] = self.vl_white
            current_config["vl_red"] = self.vl_red
            current_config["vl_green"] = self.vl_green
            current_config["vl_blue"] = self.vl_blue
            current_config["natural_light"] = self.natural_light
            current_config["circadian_cycle"] = self.circadian_cycle
            current_config["progressive_light"] = self.progressive_light

            with open("/home/"+ str(file_name) + ".txt", "a") as f:
                f.writelines("{}:{}\n".format(k,v) for k,v in current_config.items())

            print("Saved " + file_name)
            popup.dismiss()

        file_name = ""

        popup_content = BoxLayout(orientation='vertical')
        buttons_box = BoxLayout(orientation='horizontal')

        ok_button = Button(text="Ok", font_size = 14)
        cancel_button = Button(text="Cancel", font_size = 14)

        ok_button.bind(on_press = ok)
        cancel_button.bind(on_press = cancel)

        buttons_box.add_widget(ok_button)
        buttons_box.add_widget(cancel_button)

        text_input = TextInput(focus=False, multiline=False)

        popup_content.add_widget(text_input)
        popup_content.add_widget(buttons_box)

        popup = Popup(title="Preference name", content= popup_content, size_hint = (0.3, 0.2))
        popup.open()


class Luminaria(App):
    def build(self):
        ui = UI()
        return ui


def exit_handler():
    print("Closing socket")
    sock.close()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ("localhost", 10003)
    print("Connection to {} port {}".format(server_address[0],server_address[1]))
    sock.connect(server_address)
    Luminaria().run()
    atexit.register(exit_handler)
