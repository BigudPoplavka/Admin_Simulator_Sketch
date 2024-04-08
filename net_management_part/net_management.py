import tkinter as tk
from PIL import Image, ImageTk

from control_modes import *
from net_elements import *
from connections_list import *


class NetworkFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg="white", width=600, height=400, bd=1, relief="solid")
        self.devices_panel = None
        self.width = self.canvas.winfo_width()
        self.height = self.canvas.winfo_height()
        self.canvas.pack(fill="both", expand=True)
        self.changeble_on_mode_objects = []
        self.curr_mode = add_object_mode
        self.curr_device_creaction_func = create_router
        self.drag_mode = False
        self.last_x = 0
        self.last_y = 0
        self.min_clipping_offset = 50
        self.dragging = None
        self.selected_object = None
        self.objects = []
        self.objects_id = 0
        self.connections = []
        self.connections_id = 0
        self.connections_list = None
        self.connections_listbox = None
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def set_selected_object(self, obj):
        self.selected_object = obj

    def clear_selected_object(self):
        self.selected_object = None

# ПЕРЕКЛЮЧЕНИЕ КОНТРОЛ-МОДА

    def set_disabled_modes(self):
        for mode in modes_list:
            if self.curr_mode == mode:
                continue
            mode.disable()

    def set_mode(self, mode):
        self.curr_mode = mode
        self.curr_mode.active()
        self.set_disabled_modes()

    def set_add_object_mode(self):
        self.set_mode(add_object_mode)

    def set_drag_mode(self):
        self.set_mode(drag_object_mode)

# КНОПКИ ПЕРЕКЛЮЧЕНИЯ ТИПА УСТРОЙСТВА
        
    def pick_router(self):
        self.curr_device_creaction_func = create_router

    def pick_switch(self):
        self.curr_device_creaction_func = create_switch

    def pick_server(self):
        self.curr_device_creaction_func = create_server

# ЛОГИКА РАБОТЫ МОДОВ
        
    def add_object(self, x, y):
        if x + 10 >= self.canvas.winfo_width():
            x = self.canvas.winfo_width() - self.min_clipping_offset

        if y + 10 >= self.canvas.winfo_height():
            y = self.canvas.winfo_height() - self.min_clipping_offset

        self.objects_id += 1
        obj = self.curr_device_creaction_func(self, self.canvas, x, y, self.objects_id)

        self.objects.append(obj)

        if len(self.objects) == 1:
            set_work_canvas(self.canvas)
        
    def on_canvas_click(self, event):
        x, y = event.x, event.y
        print(f"canvas pressed: {x}, {y}")

        if check_new_connection() != -1:
            if self.curr_mode != drag_object_mode:
                self.add_object(x, y)

# ДОБАВЛЕНИЕ И УДАЛЕНИЕ СОЕДИНЕНИЯ
                
    def add_connection(self, connection):
        self.connections_id += 1
        self.connections.append({'id': self.connections_id,          'connection': connection, 'listbox_item': None})
        self.connections_list.add_connection(self.connections_id, connection)
        self.connections[-1]['listbox_item'] = self.connections_list.listbox.get(tk.END)

    def delete_connection(self):
        selection = self.connections_listbox.curselection()

        if selection:
            index = selection[0]
            del_connection = None
            selection_text = self.connections_listbox.get(selection)

            for elem in self.connections:
                if elem['listbox_item'] == selection_text:
                    del_connection = elem
                    break

            del_connection_devices = [
                del_connection['connection'].device_id_1,
                del_connection['connection'].device_id_2
            ]

            del_connection_ports = [
                del_connection['connection'].port_index_1,
                del_connection['connection'].port_index_2
            ]

            del_connection_devices[0].ports[del_connection_ports[0] - 1].disconnect_cable()

            del_connection_devices[1].ports[del_connection_ports[1] - 1].disconnect_cable()

            self.connections_listbox.delete(index)
            self.canvas.delete(del_connection['connection'].line_id)
            self.connections.remove(del_connection)

    
def get_net_management_window(master):
    work_frame = NetworkFrame(master, width=760)
    work_frame.pack(fill="both", expand=True, side="top")

# ПАНЕЛИ ОКНА
    
    menubar = tk.Frame(work_frame, background="#D4D4D4", height=20)
    menubar.pack(fill="both", expand=True, side="top")

    devices_panel = tk.Frame(menubar, background="#C3C3C3", padx=5, pady=5)
    devices_panel.pack(fill="y", expand=True, side="right")

    modes_panel = tk.Frame(menubar, background="#D4D4D4", padx=5, pady=5)
    modes_panel.pack(fill="y", expand=True, side="left")
        
    connections_list_panel = tk.Frame(menubar, background="#C3C3C3", padx=5, pady=5)
    connections_list_panel.pack(fill="y", expand=True, side="left")

# КНОПКИ ВЫБОРА УСТРОЙСТВА ИЛИ СОЕДИНИТЕЛЯ

    new_switch = tk.Button(devices_panel, 
                        text="new_switch", 
                        command=work_frame.pick_switch)
    new_switch.pack(pady=1, fill="y")

    new_router = tk.Button(devices_panel, 
                        text="new_router", 
                        command=work_frame.pick_router)
    new_router.pack(pady=1, fill="y")

    new_server = tk.Button(devices_panel, 
                        text="new_server", 
                        command=work_frame.pick_server)
    new_server.pack(pady=1, fill="y")

# КНОПКИ ПЕРЕКЛЮЧЕНИЯ МОДА

    add_mode_button = tk.Button(modes_panel, 
                        text="➕", 
                        command=work_frame.set_add_object_mode)
    add_mode_button.pack(pady=1, fill="y")

    drag_mode_button = tk.Button(modes_panel, 
                        text="✋", 
                        command=work_frame.set_drag_mode)
    drag_mode_button.pack(pady=1, fill="y")

    delete_mode_button = tk.Button(modes_panel, 
                            text="✖",
                            command=work_frame.set_mode(del_object_mode))
    delete_mode_button.pack(pady=1, fill="y")

    add_object_mode.active_elements = [add_mode_button]
    drag_object_mode.active_elements = [drag_mode_button]
    del_object_mode.active_elements = [delete_mode_button]

    work_frame.set_mode(add_object_mode)

# СОЕДИНЕНИЯ 
    
    connection_list = ConnectionList(connections_list_panel, work_frame.connections)
    connection_list.pack()

    work_frame.connections_list = connection_list
    work_frame.connections_listbox = connection_list.listbox

    delete_button = tk.Button(connections_list_panel, text="⛔", command=work_frame.delete_connection)
    delete_button.pack(side="right")

    return work_frame
