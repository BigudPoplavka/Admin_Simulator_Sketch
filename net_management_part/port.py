from enum import Enum
from addresses import *


class PortState:
    def __init__(self, name, code, indicator_color, status):
        self.name = name
        self.code = code
        self.indicator_color = indicator_color
        self.status = status


class StateCode(Enum):
    DISABLED = 0
    CONNECTED = 1
    DISCONNECTED = 2


class Status(Enum):
    UP = 0,
    DOWN = 1,
    ADMINISTRATICELY_DOWN = 2,
    UP_DOWN = 3,
    DOWN_DOWN = 4

statuses = {
            Status.UP: 'up',
            Status.DOWN: 'down',
            Status.ADMINISTRATICELY_DOWN: 'administratively down',
            Status.UP_DOWN: 'up/down',
            Status.DOWN_DOWN: 'down/down'
        }

port_disabled = PortState("Disabled", -1, '#585858', Status.DOWN_DOWN)
port_connected = PortState("Connected", 1, '#79F260', Status.UP)
port_disconnected = PortState("Disconnected", 0, '#F04238', Status.DOWN)

class Port:
    def __init__(self, port_id, state):
        self.port_id = port_id
        self.state = state
        self.vlan = None  
        self.is_cable_connected = False
        self.is_configured = False
        self.ip = IPAddress(0, 0, 0, 0)
        self.config = {
            'ip':self.ip,
            'vlan':self.vlan,
            'state':self.state
        }

    def set_port_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def connect_cable(self):
        self.is_cable_connected = True

    def disconnect_cable(self):
        self.is_cable_connected = False
        self.disconnect()

    def is_connected(self):
        return self.is_cable_connected
    
    def enable(self):
        self.state = port_connected

    def disconnect(self):
        self.state = port_disconnected
        print(f"Port {self.port_id} disconnected")

    def turn_off(self):
        self.state = port_disabled

    def configure(self):
        print(f"Port {self.port_id} configured")

        if self.check_config():
            self.enable()
        else:
            self.disconnect()
        
    def check_config(self):
        if self.ip.subnet_1 != self.ip.subnet_2 != 0:
            
            return True
        else:

            return False
        

class Connection:
    def __init__(self, line_id, device_id_1, device_id_2, port_index_1, port_index_2):
        self.line_id = line_id
        self.device_id_1 = device_id_1
        self.device_id_2 = device_id_2
        self.port_index_1 = port_index_1
        self.port_index_2 = port_index_2
        


