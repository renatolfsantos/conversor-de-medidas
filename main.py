from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder


class MainWindow(Screen):

    def set_tipo(self, tipo):
        unidades = []
        self.tipo = tipo
        self.ids.titulo.text = f"Conversão de {tipo.capitalize()}"

        if tipo == "comprimento":
            unidades = ["m", "km", "cm"]
        elif tipo == "massa":
            unidades = ["kg", "g", "mg"]
        elif tipo == "temperatura":
            unidades = ["C", "F", "K"]
        elif tipo == "volume":
            unidades = ["L", "mL"]

        self.ids.de_unidade.values = unidades 
        self.ids.para_unidade.values = unidades

    def converter(self):
        try:
            valor = float(self.ids.input_valor.text)
            de = self.ids.de_unidade.text
            para = self.ids.para_unidade.text

            resultado = valor

            if self.tipo == "comprimento":
                fatores = {"m":1, "km":1000, "cm":0.01}
                resultado = valor * fatores[de] / fatores[para]

            elif self.tipo == "massa":
                fatores = {"kg":1, "g":0.001, "mg":0.000001}
                resultado = valor * fatores[de] / fatores[para]

            elif self.tipo == "volume":
                fatores = {"L":1, "mL":0.001}
                resultado = valor * fatores[de] / fatores[para]

            elif self.tipo == "temperatura":
                if de == "C" and para == "F":
                    resultado = valor * 9/5 + 32
                elif de == "F" and para == "C":
                    resultado = (valor - 32) * 5/9
                elif de == "C" and para == "K":
                    resultado = valor + 273.15
                elif de == "K" and para == "C":
                    resultado = valor - 273.15
                else:
                    resultado = valor

            self.ids.resultado.text = f"Resultado: {resultado:.2f} {para}"

        except:
            self.ids.resultado.text = "Erro na conversão"
            
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


kv_files = [
    "welcome.kv",
    "main.kv"
]

for kv in kv_files:
    Builder.load_file(kv)


sm = ScreenManager()

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