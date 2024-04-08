import tkinter as tk
import re
from enum import Enum

from test_task import *

class ConsoleMode(Enum):
    default = 0, 
    exec = 1,
    conf = 2, 
    conf_vlan = 3,
    conf_if = 4

class ConsoleEmulator(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.commands = []
        self.correct_sequence = None
        self.current_command_index = 0
        self.device_name = 'Switch'
        self.task = None
        self.is_config_mode = False
        self.mode_suffix = [">", "#", "(config)#", "(config-vlan)#"]
        self.modes = {
            'default': self.mode_suffix[0],
            'exec': self.mode_suffix[1],
            'conf': self.mode_suffix[2],
            'conf_vlan': self.mode_suffix[3]
        }
        self.curr_mode = 'default'

        self.input_field = tk.Text(self, bg="black", fg="green", font=("Courier", 12))
        self.input_field.pack(fill=tk.BOTH, expand=True)
        self.input_field.bind("<Return>", self.on_enter)
        self.input_field.bind("<Key>", self.on_entry_key_press)
        self.input_field.insert(tk.END, f"{self.device_name}>") 
        self.status_label = tk.Label(self, text="Статус настройки")
        self.status_label.pack(side=tk.LEFT)
        self.progress = tk.Label(self, text="0")
        self.progress.pack(side=tk.LEFT)
        self.percent = tk.Label(self, text="%")
        self.percent.pack(side=tk.LEFT)
        self.status_indicator = tk.Label(self, text="  ", bg="grey", width=2, padx=10)
        self.status_indicator.pack(side=tk.LEFT)
        self.reset_button = tk.Button(self, 
                                      text="🔄", 
                                      command=self.reset)
        self.reset_button.pack(side=tk.LEFT)

    def set_task(self, task):
        self.task = task
        self.correct_sequence = task.correct_sequence

    def reset(self):
        self.current_command_index = 0
        self.progress.configure(text="0")
        self.status_indicator.configure(bg="grey")
        self.input_field.delete(1.0, tk.END)
        self.input_field.insert(1.0, f"{self.device_name}>")
        self.curr_mode = 'default'

    def get_last_char_before_cursor(self, entry):
        cursor_pos = entry.index(tk.INSERT)

        if cursor_pos != "1.0":
            prev_char_pos = entry.index(f"{cursor_pos} - 1 chars")

            return entry.get(prev_char_pos, cursor_pos)

    def on_enter(self, event):
        current_text = self.input_field.get("end-2l", "end-1c")

        if current_text.strip() == f"{self.device_name}{self.modes[self.curr_mode]}":
            return

        self.process_command(event)

    def on_entry_key_press(self, event):
        last_symbol = self.get_last_char_before_cursor(self.input_field)

        if event.keysym == "BackSpace":
            if last_symbol == ">":
                self.input_field.insert(tk.END, ">")
                return 
            elif last_symbol == "#":
                self.input_field.insert(tk.END, "#")
                return 

    def process_command(self, event):
        pattern = ''
        curr_mode = ''
        prefix = f"{self.device_name}{self.modes[self.curr_mode]}"
        command = self.input_field.get("end-2l", "end-1c")

        # когда в статусе есть скобки надо их экранировать в паттерне

        if self.modes[self.curr_mode].startswith('('):
            curr_mode = f"\{self.modes[self.curr_mode][:-2]}\{self.modes[self.curr_mode][-2:]}"
        else:
            curr_mode = f"{self.modes[self.curr_mode]}"

        if command.startswith(prefix +'\n'):
            pattern = f"{self.device_name}" + curr_mode + '\n' + "(.*)" 
        elif command.startswith(prefix):
            pattern = f"{self.device_name}" + curr_mode + "(.*)" 
        elif command.startswith('\n' + prefix):
            pattern = f"\n{self.device_name}" + curr_mode + "(.*)"
        else:
            pattern = "(.*)\n" + prefix

        command = re.search(pattern, command)

        if command and command != '':
            command = command.group(1)
        else:
            command = self.input_field.get("end-2l", "end-1l")

        if command.startswith(prefix):
            command = command.removeprefix(prefix)
        if command.endswith(prefix):
            command = command.removesuffix(prefix)
        if command.endswith('\n'):
            command = command.removesuffix('\n')

        print(f"command: {command}")

        self.commands.append(command)

        tmp = self.modes[self.curr_mode]
        status_changes = self.task.get_status(command, self.current_command_index)

        if re.match(self.correct_sequence[self.current_command_index], command):
            if status_changes:
                self.curr_mode = status_changes
                self.input_field.insert("end", f"\n{self.device_name}{self.modes[status_changes]}")
            
            self.current_command_index += 1
            percent = self.current_command_index / len(self.correct_sequence) * 100
            self.progress.configure(text=f"{int(percent)}")
        else:
            try:
                self.input_field.insert("end", f"\n{self.device_name}{self.modes[status_changes]}")
                return
            except KeyError:
                self.input_field.insert("end", f"\n{self.device_name}{tmp}")
                return

        if self.current_command_index == len(self.correct_sequence):
            self.status_indicator.config(bg="green")
            self.commands.clear()
        else:
            self.status_indicator.config(bg="grey")


def get_emulator_window(master):
    console_emulator = ConsoleEmulator(master)
    return console_emulator
