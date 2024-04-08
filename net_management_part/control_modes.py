class Mode():
    def __init__(self, title, active_elements):
        self.title = title
        self.active_elements = active_elements

    def active(self):
        for elem in self.active_elements:
            elem.configure(background="#99EA67")

    def disable(self):
        for elem in self.active_elements:
            elem.configure(background="#757575")


add_object_mode = Mode("Add", [])
drag_object_mode = Mode("Drag", [])
del_object_mode = Mode("Delete", [])

modes_list = [
    add_object_mode,
    drag_object_mode,
    del_object_mode
]