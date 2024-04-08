import tkinter as tk
from PIL import Image, ImageTk
from enum import Enum
from tkinter import messagebox

from port import *
from control_modes import *
from devices import *
from addresses import *
from console import *


class DeviceType(Enum):
    ROUTER = 1,
    SWITCH = 2,
    SERVER = 3,
    PC = 4

router_icon_path = "UI\\network_devices\\router_1.png"
switch_icon_path = "UI\\network_devices\switch_1.png"
server_icon_path = "UI\\network_devices\server_1.png"
router_icon = Image.open(router_icon_path)
switch_icon = Image.open(switch_icon_path)
server_icon = Image.open(server_icon_path)

device_type_icon = {
    DeviceType.ROUTER: router_icon,
    DeviceType.SWITCH: switch_icon,
    DeviceType.SERVER: server_icon
}

new_connection_started = False
tmp_connection_device_1, tmp_connection_device_2 = None, None 
connections_canvas = None

def set_work_canvas(canvas):
    global connections_canvas
    connections_canvas = canvas


def check_new_connection():
        global tmp_connection_device_1
        global tmp_connection_device_2
        global new_connection_started

        if new_connection_started:
            tmp_connection_device_1 = None
            new_connection_started = False
            print("Сброшено")
            return -1


def connect_devices(parent, device_and_port_1, device_and_port_2):
    if len(device_and_port_1[0].connections) == device_and_port_1[0].max_connections or len(device_and_port_2[0].connections) == device_and_port_2[0].max_connections:
        messagebox.showwarning("Внимание!", "Все порты заняты!")
        return

    offset = 5 if len(device_and_port_1[0].connections) == 1 else 0

    start_x = device_and_port_1[0].frame.winfo_x() + device_and_port_1[0].frame.winfo_width() / 2
    start_y = device_and_port_1[0].frame.winfo_y() + device_and_port_1[0].frame.winfo_height() / 2
    end_x = device_and_port_2[0].frame.winfo_x() + device_and_port_2[0].frame.winfo_width() / 2
    end_y = device_and_port_2[0].frame.winfo_y() + device_and_port_2[0].frame.winfo_height() / 2

    start_y = start_y + offset
    end_y = end_y + offset

    line_id = connections_canvas.create_line(start_x, start_y, end_x, end_y)

    device_and_port_1[1].connect_cable()
    device_and_port_2[1].connect_cable()

    connection = Connection(line_id, 
                            device_and_port_1[0].device, 
                            device_and_port_2[0].device, 
                            device_and_port_1[1].port_id, 
                            device_and_port_2[1].port_id,
                )

    device_and_port_1[0].connections.append(connection)
    device_and_port_2[0].connections.append(connection)

    parent.add_connection(connection)


# ФРЕЙМ СЕТЕВОГО УСТРОЙСТВА СО ВСЕМ СОДЕРЖИМЫМ

class DeviceFrame:
    def __init__(self, parent, canvas, x, y, icon, name, ports):
        self.parent = parent
        self.canvas = canvas
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_x = self.canvas.winfo_rootx()
        self.canvas_y = self.canvas.winfo_rooty()
        self.x = x
        self.y = y
        self.last_x = 0
        self.last_y = 0
        self.icon = icon
        self.name = name
        self.enabled = False 
        self.ports = ports
        self.device = None
        self.max_connections = 0
        self.connections = []
        self.create_frame()
        self.create_ports()

    def create_frame(self):
        self.frame = tk.Frame(self.canvas)
        self.widget_id = self.canvas.create_window(self.x, self.y, window=self.frame, anchor="nw")

        icon = ImageTk.PhotoImage(self.icon)
        self.icon = icon

        self.icon_label = tk.Label(self.frame, image=self.icon, compound="center")
        self.icon_label.grid(row=0, column=0)
        self.name_label = tk.Label(self.frame, text=self.name, bg="white")
        self.name_label.grid(row=1, column=0, pady=2)

        self.ports_frame = tk.Frame(self.frame, bg="white")
        self.ports_frame.grid(row=3, column=0, columnspan=len(self.ports), padx=1, pady=1)

        self.power_button = tk.Button(self.frame, 
                                      width=10, 
                                      text="🗲", 
                                      command=self.on_power_button_click)
        self.power_button.grid(row=2, column=0, rowspan=1, columnspan=2)

        self.icon_label.bind("<Button-1>", self.on_press)
        self.icon_label.bind("<B1-Motion>", self.on_drag)
        self.icon_label.bind("<ButtonRelease-1>", self.on_release)
        self.icon_label.bind("<Button-3>", self.open_console)  
        
    def on_power_button_click(self):
        self.enabled = not self.enabled

        if self.enabled:
            self.power_button.configure(background=port_connected.indicator_color)

            for port in self.ports:
                port.configure()
        # for port_button in self.port_buttons:
        #     port_button.background = self.ports[]
        else:
            self.power_button.configure(background=port_disabled.indicator_color)
            
            for port in self.ports:
                port.turn_off()
            for port_button in self.port_buttons:
                port_button.configure(background=port_disabled.indicator_color)

# ПОРТЫ

    def create_ports(self):
        self.port_buttons = []
        self.max_connections = len(self.ports)

        for i, port in enumerate(self.ports):
            color = port.state.indicator_color
            port_button = tk.Button(self.ports_frame, 
                                  text=f"{port.port_id}", 
                                  font=("Arial", 7), 
                                  bg=color, 
                                  padx=1, pady=1, 
                                  width=1, height=1,
                                  borderwidth=0,
                                  command=lambda i=port: self.select_port(i)
                                  )
            port_button.grid(row=i // 4, column=i % 4, padx=1, pady=1)
            self.port_buttons.append(port_button)

        self.selected_port = None

# ОБРАБОТЧИКИ КНОПОК ПОРТОВ
        
    def select_port(self, port):
        self.selected_port = port

        if self.selected_port.is_connected():
            messagebox.showwarning("Внимание!", "Порт занят!")
            return

        global tmp_connection_device_1
        global tmp_connection_device_2
        global new_connection_started

        if not new_connection_started:
            tmp_connection_device_1 = (self, self.selected_port)
            new_connection_started = True
            print(f"D1 - Selected id {self.device.device_id} port {port.port_id}")
        else:
            tmp_connection_device_2 = (self, self.selected_port)
            print(f"D2 - Selected id {self.device.device_id} port {port.port_id}")

            if tmp_connection_device_1[0] == tmp_connection_device_2[0]:
                print("Порты одного и того же устройства")
                return
            
            connect_devices(self.parent, tmp_connection_device_1, tmp_connection_device_2)

            new_connection_started = False

# КОНСОЛЬ (ТЕРМИАЛ) 

    def open_console(self, event):
        self.console_frame = tk.Toplevel(self.frame)
        self.console_frame.geometry("550x250")
        self.console_input = tk.Text(self.console_frame, 
                                     wrap="word", 
                                     bg="black", 
                                     fg="#5DFF40")
        self.console_input.pack(fill=tk.BOTH, expand=True)

        self.console = Console(self.name, self.console_input)

        self.console_input.bind("<Return>", self.console.on_enter)
        self.console_input.bind("<Key>", self.console.on_entry_key_press)
        self.console_input.insert(tk.END, f"{self.name}>") 
        self.console_frame.grab_set()

# DRAG-N-DROP
            
    def on_press(self, event):
        self.dragging = True
        self.last_x = event.x_root
        self.last_y = event.y_root
        self.parent.set_selected_object(self.frame)

    def on_drag(self, event):
        if self.dragging:
            if self.parent.curr_mode == drag_object_mode and self.parent.selected_object != None:
                dx = event.x_root - self.last_x
                dy = event.y_root - self.last_y

                self.canvas_x = self.canvas.winfo_rootx()
                self.canvas_y = self.canvas.winfo_rooty()
            
                if self.canvas_x < self.frame.winfo_rootx() + dx and self.frame.winfo_rootx() + self.frame.winfo_width() + dx < self.canvas_x + self.canvas_width and self.canvas_y < self.frame.winfo_rooty() + dy and self.frame.winfo_rooty() + self.frame.winfo_height() + dy < self.canvas_y + self.canvas_height:
                    
                    self.canvas.move(self.widget_id, dx, dy)
                    self.last_x = event.x_root
                    self.last_y = event.y_root

                    for connection in self.connections:
                        line = connection.line_id
                        line_coords = self.canvas.coords(line)

                        if self.device == connection.device_id_1:
                            self.canvas.coords(line, 
                                self.last_x - (self.frame.winfo_width() + self.frame.winfo_width()/2), 
                                self.last_y - (self.frame.winfo_height()/2), 
                                line_coords[2], 
                                line_coords[3])
                        elif self.device == connection.device_id_2:
                            self.canvas.coords(line, 
                                line_coords[0], 
                                line_coords[1],
                                self.last_x - (self.frame.winfo_width() + self.frame.winfo_width()/2), 
                                self.last_y - (self.frame.winfo_height()/2))

    def on_release(self, event):
        self.dragging = False
        self.parent.clear_selected_object()

def update_line(self, device1, device2):
    x1, y1 = self.canvas.coords(device1)
    x2, y2 = self.canvas.coords(device2)

    self.canvas.coords(self.line, x1, y1, x2, y2)

# СОЗДАНИЕ СЕТЕВЫХ УСТРОЙСТВ

def create_router(parent, canvas, x, y, id):
    router = DeviceFrame(parent, canvas, x, y, 
                    device_type_icon[DeviceType.ROUTER], "Router", 
                    [
                        Port(port_id=1, state=port_disabled),
                        Port(port_id=2, state=port_disabled),
                        Port(port_id=3, state=port_disabled),
                        Port(port_id=4, state=port_disabled)
                    ])
    router.device = Router("Router", 
                           IPAddress(0, 0, 0, 0), IPAddress(255, 255, 255, 0),
                           None, 
                           router.ports)
    router.device.device_id = id
    router.name_label.configure(text= f"{router.name} {id}")

    return router

def create_switch(parent, canvas, x, y, id):
    switch = DeviceFrame(parent, canvas, x, y, 
                        device_type_icon[DeviceType.SWITCH], "Switch", 
                    [
                        Port(port_id=1, state=port_disabled),
                        Port(port_id=2, state=port_disabled),
                        Port(port_id=3, state=port_disabled),
                        Port(port_id=4, state=port_disabled)
                    ])
    switch.device = Switch("Switch", 
                           IPAddress(0, 0, 0, 0), IPAddress(255, 255, 255, 0),
                           None, 
                           switch.ports)
    switch.device.device_id = id
    switch.name_label.configure(text=f"{switch.name} {id}")

    return switch

def create_server(parent, canvas, x, y, id):
    server = DeviceFrame(parent, canvas, x, y, 
                        device_type_icon[DeviceType.SERVER], "Server", 
                    [
                        Port(port_id=1, state=port_disabled),
                        Port(port_id=2, state=port_disabled),
                        Port(port_id=3, state=port_disabled),
                        Port(port_id=4, state=port_disabled),
                        Port(port_id=5, state=port_disabled),
                        Port(port_id=6, state=port_disabled),
                        Port(port_id=7, state=port_disabled),
                        Port(port_id=8, state=port_disabled),
                    ])
    server.device = Switch("Switch", 
                           IPAddress(0, 0, 0, 0), IPAddress(255, 255, 255, 0),
                           None, 
                           server.ports)
    server.device.device_id = id
    server.name_label.configure(text=f"{server.name} {server.device.device_id}")

    return server

def create_PC(parent, canvas, x, y):
    pass