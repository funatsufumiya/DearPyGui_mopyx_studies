from mopyx import model, render, render_call, action, computed
import dearpygui.dearpygui as dpg
from typing import List

@model
class Model:
    def __init__(self):
        self.count: int = 0
        self.texts: List[str] = []

    def update_texts(self):
        # print("init_texts")
        if len(model.texts) < model.count:
            n = len(model.texts)
            for i in range(model.count - n):
                model.texts.append(f"Hello World {n + i + 1}")
        elif len(model.texts) > model.count:
            model.texts = model.texts[:model.count]

model = Model()

class MainWindow():
    n = 0

    def __init__(self):
        self.setupUi()
        self.update_from_model()

    # def button_callback(self, sender, app_data, user_data):
    #     if sender == "btn":
    #         self.n += 1
    #         self.change_text(f"Hello World {self.n}")
    
    def slider_callback(self, sender, app_data, user_data):
        if sender == "count":
            self.change_count(dpg.get_value(sender))

    def text_input_callback(self, sender, app_data, user_data):
        if sender.startswith("text"):
            i = int(sender[4:])
            model.texts[i] = dpg.get_value(sender)

    def setupUi(self):
        dpg.create_context()

        with dpg.window(label="Main Window", tag="mainWindow"):
            # dpg.add_text("", tag="text")
            dpg.add_slider_int(label="Count", tag="count", max_value=10, min_value=0, callback=self.slider_callback)

            # texts container
            with dpg.child_window(tag="texts", width=-1, height=-1):
                pass


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
        self.update_count()
        self.update_texts()

    # @render
    # def update_text(self):
    #     print("update_text")
    #     dpg.set_value("text", model.text)

    @render
    def update_count(self):
        print("update_count")
        dpg.set_value("count", model.count)

    last_text_count = 0

    @render
    def update_texts(self):
        print(f"update_texts: {model.texts}")
        for i, text in enumerate(model.texts):
            if dpg.does_item_exist(f"text{i}"):
                dpg.set_value(f"text{i}", text)
            else:
                # dpg.add_text("", tag=f"text{i}", parent="texts")
                dpg.add_input_text(tag=f"text{i}", parent="texts", default_value=text, callback=self.text_input_callback)

        if len(model.texts) < self.last_text_count:
            for i in range(len(model.texts), self.last_text_count):
                dpg.delete_item(f"text{i}")

        self.last_text_count = len(model.texts)
            

    # def change_text(self, text):
    #     model.text = text

    @action
    def change_count(self, count):
        model.count = count
        model.update_texts()


def main():
    MainWindow().show()

if __name__ == '__main__':
    main()