import tkinter as tk
from tkinter import Scrollbar


class ConnectionList(tk.Frame):
    def __init__(self, master, connections):
        super().__init__(master)
        self.connections = connections
        self.listbox = tk.Listbox(self, width=70, height=10)
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.populate_listbox()

    def add_connection(self, connection_id, connection):
        self.listbox.insert("end", f"Connect {connection_id} ( {connection.device_id_1.name} {connection.device_id_1.device_id} port {connection.port_index_1} --- {connection.device_id_2.name} {connection.device_id_2.device_id} port {connection.port_index_2})")

    def populate_listbox(self):
        for connection_id, connection_data in self.connections:
            self.listbox.insert("end", f"{connection_id} ({connection_data.device_id_1.name} port {connection_data.port_index_1} ---  {connection_data.device_id_2.name} port {connection_data.port_index_2})")

    def delete_connection(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            self.listbox.delete(index)
            del self.connections[index]


