class Device:
    def __init__(self, name, ip, subnet_mask, mac, ports):
        self.name = name
        self.ip = ip
        self.subnet_mask = subnet_mask
        self.mac = mac
        self.ports = ports
        self.device_id = -1


class NetworkDevice(Device):
    def __init__(self, name, ip, subnet_mask, mac, ports):
        super().__init__(name, ip, subnet_mask, mac, ports)

        self.service_password_encryption = False
        

        self.network_devices_common_commands = {
            "enable": self.enable,
            "show running-config": self.show_running_config,
            "show interfaces": self.show_interfaces,
            "show ip interface brief": self.show_ip_interface_brief,
            "show vlan": self.show_vlan,
            "show mac address-table": self.show_mac_address_table, 
            "show arp": self.show_arp,
            "ping": self.ping,
            "traceroute": self.traceroute
        }

    def get_bool_state_str(state, str_values):
        if state:
            return str_values[0]
        return str_values[1]

    def show_running_config(self):
        interfaces_data = []
        security = self.get_bool_state_str(self.service_password_encryption, ["password", "no service password-encryption"])

        result = f"Building configuration...\nCurrent configuration:\n!\nversion 12.2\nno service pad\nservice timestamps debug uptime\nservice timestamps log uptime\n {security}\n!\nhostname {self.name}\n!\n!\n!\n"
        return result
    
    def enable(self):
        return

    def show_running_config(self):
        return
        
    def show_interfaces(self):
        return
        
    def show_ip_interface_brief(self):
        return
        
    def show_vlan(self):
        return
        
    def show_mac_address_table(self):
        return
        
    def show_arp(self):
        return
        
    def ping(self):
        return
        
    def traceroute(self):
        return


# ROUTER ********************************************************        

class Router(NetworkDevice):
    def __init__(self, name, ip, subnet_mask, mac, ports):
        super().__init__(name, ip, subnet_mask, mac, ports)

# SWITCH ********************************************************  

class Switch(NetworkDevice):
    def __init__(self, name, ip, subnet_mask, mac, ports):
        super().__init__(name, ip, subnet_mask, mac, ports)

# SERVER ********************************************************  

class Server(NetworkDevice):
    def __init__(self, name, ip, subnet_mask, mac, ports):
        super().__init__(name, ip, subnet_mask, mac, ports)

# PC ************************************************************

class PC(NetworkDevice):
    def __init__(self, name, ip, subnet_mask, mac, ports):
        super().__init__(name, ip, subnet_mask, mac, ports)