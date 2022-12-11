from mopyx import model, render, render_call, action
import dearpygui.dearpygui as dpg

@model
class Model:
    def __init__(self):
        self.text = 'Hello World'

model = Model()

class MainWindow():
    n = 0

    def __init__(self):
        self.setupUi()
        self.update_from_model()

    def button_callback(self, sender, app_data, user_data):
        if sender == "btn":
            self.n += 1
            self.change_text(f"Hello World {self.n}")
            # model.text = f"Hello World {n}"

    def setupUi(self):
        dpg.create_context()

        with dpg.window(label="Main Window", tag="mainWindow"):
            dpg.add_text("", tag="text")
            dpg.add_button(label="Change Text", tag="btn", callback=self.button_callback)

        dpg.create_viewport(title=f"Add Gui Example", width=800, height=600)
        dpg.setup_dearpygui()

        dpg.set_primary_window("mainWindow", True)

    def show(self):
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    @render
    def update_from_model(self):
        print("update_from_model")
        self.update_text()

    @render
    def update_text(self):
        print("update_text")
        dpg.set_value("text", model.text)

    def change_text(self, text):
        model.text = text

def main():
    MainWindow().show()

if __name__ == '__main__':
    main()