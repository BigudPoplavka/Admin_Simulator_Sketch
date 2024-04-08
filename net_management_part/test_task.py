from console_emulator import ConsoleMode
import re

class EmulatorTask():
    def __init__(self, title, correct_sequence):
        self.title = title
        self.description = None
        self.commands = []
        self.correct_sequence = correct_sequence
        self.modes_changes = {
            0: 'exec',
            1: 'conf',
            2: 'conf_vlan'
        }

    def get_status(self, command, command_index):
        if command_index in self.modes_changes.keys():
            if re.match(self.correct_sequence[command_index], command):
                return self.modes_changes[command_index]
            return None
        return None

task_vlan = EmulatorTask('Настройка VLAN', [r'(ena|enable)', r'(conf t|configure terminal)',
    r'vlan\s(?:[1-9]\d{0,3}|[1-3]\d{4}|40(?:[0-8]\d{2}|9(?:[0-5]\d|96)))', r'name \S{1,10}', 
    'exit'])
task_vlan.description = "1. Войдите в привелегированный режим\n2. Войдите в режим конфигурации\n3. Введите правильные команды для настройки vlan на порте"
