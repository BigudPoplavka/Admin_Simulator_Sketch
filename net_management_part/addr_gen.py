import random

def generate_ip_segment():
    for i in range(256):
        yield str(i)


def generate_device_ips(num_devices, device_types):
    device_ips = {}
    for i in range(num_devices):
        device_type = random.choice(device_types)
        ip = '.'.join(generate_ip_segment())
        device_ips[f"Device_{i+1}"] = {"IP": ip, "Ports_IPs": [f"{ip}.{j}" for j in range(1, 5)]}
    return device_ips


num_devices = 5
device_types = ["Switch", "Router", "PC"]

device_ips = generate_device_ips(num_devices, device_types)
for device, info in device_ips.items():
    print(f"Устройство: {device}")
    print(f"- IP: {info['IP']}")
    print(f"- IP-адреса Gigabit ethernet портов: {info['Ports_IPs']}")
    print()
