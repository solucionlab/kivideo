#Configuracion de ventana maximizada y sin bordes que inhibe 
#salirse al presionar esc y cuando le das alt+F4 te pregunta si estas seguro

from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'window_state', 'maximized')
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.core.window import Window

Builder.load_string('''
<PasswordPopup>:
    size_hint: None, None
    size: '600dp', '250dp'
    title: 'Exit'
    on_open: password.text = ''
    BoxLayout:
        size_hint: None, None
        size: '80dp', '170dp'
        orientation: 'vertical'
        Label:
            text: 'Password'
        BoxLayout:
            orientation: 'vertical'
            TextInput:
                id: password
                on_text_validate: root.verify()
                multiline: False
                use_handles: False
                password: True
                size_hint: None, None
                size: '500dp', '25dp'
                font_size: '15dp'
        BoxLayout:
            size_hint: None, None
            size: '500dp', '25dp'
            Label
                text:''
        Widget:
        BoxLayout:
            size_hint: None, None
            size: '570dp', '50dp'
            orientation: 'horizontal'
            spacing:1
            Label
                text:'        '
            Button:
                text: 'Ok'
                on_press: root.verify()
            Button:
                text: 'Cancel'
                on_press: root.dismiss()
''')

class PasswordPopup(Factory.Popup):
    def __init__(self, passwd, success_callback, **kwargs):
        self._passwd = passwd
        self._succ_cb = success_callback
        self._fail_cb = kwargs.pop('fail_callback', None)
        super(PasswordPopup, self).__init__(**kwargs)

    def verify(self, *largs):
        self.dismiss()
        passwd = self.ids.password.text
        if passwd == self._passwd:
            if callable(self._succ_cb):
                self._succ_cb(self)
        elif callable(self._fail_cb):
            self._fail_cb(self)


class TestApp(App):
    def build(self):
        Window.bind(on_request_close=self.on_request_close)
        return Factory.Label(text='Hola Tarola')

    def on_request_close(self, *largs):
        self.pp = pp = PasswordPopup('test', self.stop)
        pp.open()
        return True

TestApp().run()