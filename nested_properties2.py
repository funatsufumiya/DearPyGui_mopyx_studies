import uuid
from mopyx import model, render, render_call, action, computed
import dearpygui.dearpygui as dpg
from typing import List
from typing_extensions import TypedDict

@model
class Person:
    id: str
    name: str
    age: int
    company: str

    def __init__(self, id: str, name: str, age: int, company: str):
        self.id = id
        self.name = name
        self.age = age
        self.company = company

@model
class Model:
    def __init__(self):
        self.persons: List[Person] = []

    def append_person(self):
        p = Person(uuid.uuid4().hex, "", 20, "")
        self.persons.append(p)

model = Model()

class MainWindow():
    n = 0

    def __init__(self):
        self.setupUi()
        self.render_me()

    def add_person(self, sender, app_data, user_data):
        model.append_person()

    def setupUi(self):
        dpg.create_context()

        with dpg.window(label="Main Window", tag="mainWindow"):
            # dpg.add_text("", tag="text")
            # texts container

            with dpg.window(tag="sidemenu", label="side menu", width=200, height=-1, pos=(0, 20), no_close=True):
                # dpg.add_text("sidemenu")
                dpg.add_button(label="add person", callback=self.add_person)

            with dpg.window(tag="persons", label="persons", width=400, height=400, pos=(200, 20), no_close=True):
                pass


        dpg.create_viewport(title=f"Add Gui Example", width=800, height=600)
        dpg.setup_dearpygui()

        dpg.set_primary_window("mainWindow", True)

    def show(self):
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def update_person_callback(self, sender, app_data, user_data):
        # print("update_person")
        id = sender.split("_")[1]
        name = dpg.get_value(f"name_{id}")
        age = dpg.get_value(f"age_{id}")
        company = dpg.get_value(f"company_{id}")
        person = next((p for p in model.persons if p.id == id), None)
        # print(f"person: {person}")
        if person:
            person.name = name
            person.age = age
            person.company = company
            

    @render
    def render_me(self):
        print("render_me")
        # self.update_count()
        self.render_persons()

    @render
    def render_persons(self):
        print("render_persons")
        for person in model.persons:
            render_call(lambda: self.render_person(person), ignore_updates=True)
            
    @render(ignore_updates=True)
    def render_person(self, person: Person):
        id = person.id
        print(f"render_person ({id})")
        # print(f"render_person ({person})")
        container_id = f"container_{id}"
        if not dpg.does_item_exist(container_id):
            with dpg.tree_node(tag=container_id, label=id, parent="persons"):
                dpg.add_text(f"id: {id}", tag=f"id_{id}")
                dpg.add_input_text(tag=f"name_{id}", label="name", default_value=person.name, callback=self.update_person_callback)
                dpg.add_drag_int(tag=f"age_{id}", label="age", default_value=person.age, callback=self.update_person_callback)
                dpg.add_input_text(tag=f"company_{id}", label="company", default_value=person.company, callback=self.update_person_callback)
        else:
            render_call(lambda: dpg.set_item_label(f"container_{person.id}", f'{person.name} ({person.id})'), ignore_updates=True)
            render_call(lambda: dpg.set_value(f"name_{person.id}", person.name), ignore_updates=True)
            render_call(lambda: dpg.set_value(f"age_{person.id}", person.age), ignore_updates=True)
            render_call(lambda: dpg.set_value(f"company_{person.id}", person.company), ignore_updates=True)


def main():
    MainWindow().show()

if __name__ == '__main__':
    main()