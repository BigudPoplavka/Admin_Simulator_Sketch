import tkinter as tk

class Console:
    def __init__(self, device_name, input_field):
        self.device_name = device_name
        self.input_field = input_field
        self.entered_commands_block = []
        self.last_command = ""

    def get_last_char_before_cursor(self, entry):
        cursor_pos = entry.index(tk.INSERT)

        if cursor_pos != "1.0":
            prev_char_pos = entry.index(f"{cursor_pos} - 1 chars")

            return entry.get(prev_char_pos, cursor_pos)

    def on_enter(self, event):
        current_text = self.input_field.get("end-2l", "end-1l")

        if current_text.strip() != f"{self.device_name}>" or self.input_field.get("end-1c") == "\n":
            self.input_field.insert("end", f"\n{self.device_name}>")

    def on_entry_key_press(self, event):
        last_symbol = self.get_last_char_before_cursor(self.input_field)

        if event.keysym == "BackSpace":
            if last_symbol == ">":
                self.input_field.insert(tk.END, ">")
                return 