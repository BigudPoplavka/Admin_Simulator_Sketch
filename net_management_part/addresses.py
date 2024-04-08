class IPAddress:
    def __init__(self, subnet_1, subnet_2, subnet_3, device_addr, slash_num=-1):
        self.addr_parts = [subnet_1, subnet_2, subnet_3, device_addr, slash_num]
        self.slash_num = slash_num

        if all(0 <= x <= 255 for x in self.addr_parts):
            self.subnet_1 = subnet_1
            self.subnet_2 = subnet_2
            self.subnet_3 = subnet_3
            self.device_addr = device_addr
        else:
            self.subnet_1 = 0
            self.subnet_2 = 0
            self.subnet_3 = 0
            self.device_addr = 0
    
    def addr_to_str(self):
        return f"{self.subnet_1}.{self.subnet_2}.{self.subnet_3}.{self.device_addr}"


class MACAddress:
    def __init__(self, part_1, part_2, part_3, part_4, part_5, part_6):
        self.addr_parts = [part_1, part_2, part_3, part_4, part_5, part_6]

    def addr_to_str(self):
        return f"{self.part_1}-{self.part_2}-{self.part_3}-{self.part_4}-{self.part_5}-{self.part_6}"


reserved_ips = [
    IPAddress(0,0,0,0,8),
    IPAddress(0,0,0,0,32),
    IPAddress(10,0,0,0,8),
    IPAddress(100,64,0,0,10),
    IPAddress(127,0,0,0,8),
    IPAddress(169,254,0,0,16),
    IPAddress(172,16,0,0,12),
    IPAddress(192,0,2,0,24),
    IPAddress(192,88,99,0,24),
    IPAddress(192,88,99,1,32),
    IPAddress(192,168,0,0,16),
    IPAddress(198,51,100,0,24),
    IPAddress(198,18,0,0,15),
    IPAddress(203,0,113,0,24),
    IPAddress(224,0,0,0,4),
    IPAddress(239,0,0,0,8),
    IPAddress(240,0,0,0,4),
    IPAddress(255,255,255,255,32)
]
        