from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty, StringProperty

class MainWindow(Screen):
    cor = ListProperty([1, 1, 1, 1])
    unidades = ListProperty([])
    tipo = StringProperty()
    
    def on_enter(self, *args):
        self.ids.de_unidade.text = "De"
        self.ids.para_unidade.text = "Para"
        self.ids.input_valor.text = ""
        self.ids.resultado.text = ""
    
    def set_tipo(self, tipo):
        self.tipo = tipo

        match tipo:
            case "comprimento":
                self.unidades = ["m", "km", "cm"]
                self.cor = [0.2, 0.6, 0.86, 0.6]
            case "massa":
                self.unidades = ["kg", "g", "mg"]
                self.cor = [0.2, 0.7, 0.4, 0.6]
            case "temperatura":
                self.unidades = ["C", "F", "K"]
                self.cor = [0.9, 0.5, 0.2, 0.6]
            case "volume":
                self.unidades = ["L", "mL"]
                self.cor = [0.6, 0.3, 0.8, 0.6]
            case _:
                self.unidades = []
                self.cor = [1, 1, 1, 1]

        self.ids.titulo.text = f"Conversão de {tipo.capitalize()}"

    def converter(self):
        valor_text = self.ids.input_valor.text
        de = self.ids.de_unidade.text
        para = self.ids.para_unidade.text

        if de == "De" or para == "Para":
            self.ids.resultado.text = "Preencha todos os campos corretamente"
            return
        
        try:
            valor = float(valor_text)
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

        except ValueError:
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