from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder


class MainWindow(Screen):
    pass

class WelcomeWindow(Screen):
    def on_enter(self, *args):
        self.update_cols()
        Window.bind(on_resize=lambda *args: self.update_cols())

    def update_cols(self):
        width = Window.width
        grid = self.ids.grid_buttons

        if width < 500:
            grid.cols = 1
        elif width < 800:
            grid.cols = 2
        else:
            grid.cols = 4

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")


sm = WindowManager()

screens = [
    WelcomeWindow(name="welcome"),
    MainWindow(name="main")
]

for screen in screens:
    sm.add_widget(screen)

class MyMainApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyMainApp().run()